import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional

import httpx

from app.config import settings
from app.services.experian_auth import obtener_token_hdc
from app.models.hdc import (
    TIPOS_CUENTA_NO_CREDITO,
    AccountEntry,
    HDCplusResponse,
    ResultadoHDC,
    ObligacionCredito,
    ScoreExperian,
    clasificar_linea_credito,
)

_BOG_TZ = timezone(timedelta(hours=-5))

TIPOS_DOCUMENTO = {
    "CC": 1,
    "NIT": 2,
    "CE": 4,
    "PAS": 5,
    "PPT": 6,
    "TI": 7,
}


async def consultar_hdc(
    numero_documento: str,
    primer_apellido: str,
    tipo_documento: str = "CC",
) -> ResultadoHDC:
    token = await obtener_token_hdc()
    url = f"{settings.experian_base_url}/cs/credit-history/v1/hdcplus"

    now = datetime.now(_BOG_TZ)
    headers = {
        "Content-Type": "application/json",
        "client_id": settings.EXPERIAN_CLIENT_ID,
        "client_secret": settings.EXPERIAN_CLIENT_SECRET,
        "Authorization": f"Bearer {token}",
        "serverIpAddress": settings.EXPERIAN_SERVER_IP,
        "ProductId": "64",
        "InfoAccountType": "1",
    }
    body = {
        "user": settings.EXPERIAN_SUBSCRIBER_USER,
        "password": settings.EXPERIAN_SUBSCRIBER_PASSWORD,
        "identifyingTrx": {
            "requestUUID": str(uuid.uuid4()),
            "dateTime": now.isoformat(),
            "originatorChannelName": settings.EXPERIAN_CHANNEL_NAME,
            "originatorChannelType": settings.EXPERIAN_CHANNEL_TYPE,
        },
        "identifyingUser": {
            "person": {
                "personId": {
                    "personIdNumber": numero_documento,
                    "personIdType": TIPOS_DOCUMENTO.get(tipo_documento.upper(), 1),
                },
                "personLastName": primer_apellido.upper(),
            }
        },
        "parameters": [
            {
                "type": "0",
                "nameParameter": "codigos",
                "valueParameter": "TOM-001",
            }
        ],
    }

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(url, json=body, headers=headers)
        resp.raise_for_status()
        raw = resp.json()

    return _procesar_respuesta(raw, numero_documento)


def _monto(v: Optional[float]) -> float:
    """Experian usa -1 para "no aplica"; se trata como 0."""
    if v is None or v < 0:
        return 0.0
    return float(v)


def _obligacion_desde_entry(entry: AccountEntry) -> Optional[ObligacionCredito]:
    """Convierte una entrada de liabilities/creditCard en ObligacionCredito.

    Estructura real HDC+ (ver docs): los valores financieros vienen en
    `values[0]`, la calidad del deudor en `featuresLiabilities` /
    `FeaturesCreditCard`, la fecha de vencimiento en `liabilitiesAccount` /
    `creditCardAccount` y el estado en `status.account`.
    """
    acct = entry.account
    if acct.accountType is None or acct.accountType in TIPOS_CUENTA_NO_CREDITO:
        return None

    linea = clasificar_linea_credito(acct.accountType, acct.subAccountType or "00")
    vals = entry.valores
    feats = entry.caracteristicas
    prod = entry.producto

    cupo = _monto(vals.initialValue) if vals else 0.0
    saldo = _monto(vals.debtBalance) if vals else 0.0
    cuota = _monto(vals.valueMonthlyPayment) if vals else 0.0

    cuotas_pagadas = vals.paidInstallments if vals else None
    total_cuotas = vals.totalNumberOfInstallments if vals else None
    cuotas_restantes = None
    if cuotas_pagadas is not None and total_cuotas:
        cuotas_restantes = max(0, total_cuotas - cuotas_pagadas)

    periodicidad = vals.periodicityOfPayments if vals else None
    if periodicidad is None:
        periodicidad = 1

    return ObligacionCredito(
        entidad_nit=str(acct.counterpartyIdNumber or ""),
        entidad_nombre=acct.nombre_entidad,
        linea_credito=linea,
        account_type=acct.accountType,
        sub_account_type=acct.subAccountType or "00",
        sub_account_type_desc=acct.subAccountTypeDesc or acct.accountTypeDesc or "",
        cupo=cupo,
        saldo=saldo,
        cuota_reportada=cuota,
        fecha_apertura=acct.accountOpeningDate,
        fecha_vencimiento=prod.expiryDate if prod else None,
        fecha_corte=vals.behaviourDate if vals else None,
        calidad_deudor=(feats.typeOfDebtor if feats and feats.typeOfDebtor else "00"),
        calidad_deudor_desc=(feats.typeOfDebtorDesc or "") if feats else "",
        periodicidad=periodicidad,
        cuotas_restantes=cuotas_restantes,
        cuotas_pagadas=cuotas_pagadas,
        total_cuotas=total_cuotas,
        cuotas_mora=(vals.installmentsOverdue or 0) if vals else 0,
        monto_mora=_monto(vals.businessValueBalanceOverdue) if vals else 0.0,
        estado_cuenta=entry.estado_cuenta or "",
        estado_cuenta_desc=entry.estado_cuenta_desc,
        vigente=entry.es_vigente,
    )


def _cedula_desde_respuesta(report) -> str:
    """Número de documento tal como lo reporta Experian, si viene."""
    for bloque in (report.basicInformation, report.identifyingAttributes):
        if bloque is not None and bloque.personId is not None:
            num = bloque.personId.personIdNumber
            if num not in (None, ""):
                return str(num).strip()
    return ""


def parsear_respuesta_hdc(raw: dict, cedula: Optional[str] = None) -> ResultadoHDC:
    """Procesa un JSON HDC+ ya obtenido (p. ej. subido por el analista).

    Si no se indica la cédula se toma la que reporta la propia respuesta.
    """
    hdc = HDCplusResponse.model_validate(raw)
    ced = (cedula or "").strip() or _cedula_desde_respuesta(hdc.ReportHDCplus)
    return _procesar_respuesta(raw, ced)


def _procesar_respuesta(raw: dict, cedula: str) -> ResultadoHDC:
    hdc = HDCplusResponse.model_validate(raw)
    report = hdc.ReportHDCplus

    if report.productResult.responseCode != 13:
        return ResultadoHDC(
            cedula=cedula,
            codigo_respuesta=report.productResult.responseCode,
            mensaje_respuesta=report.productResult.responseDesc or "",
            respuesta_original=raw,
        )

    nombre = ""
    if report.basicInformation:
        bi = report.basicInformation
        partes = [bi.names or "", bi.firstLastName or "", bi.secondLastName or ""]
        nombre = " ".join(p for p in partes if p).strip()

    # `savings` son cuentas de ahorro/corriente: no son obligaciones.
    obligaciones: list[ObligacionCredito] = []
    cerradas = 0
    for entry in report.liabilities + report.creditCard:
        ob = _obligacion_desde_entry(entry)
        if ob is None:
            continue
        if not ob.vigente:
            cerradas += 1
            continue
        obligaciones.append(ob)

    scores = []
    for m in report.models:
        if m.scoreValue is not None and m.modelCode is not None:
            scores.append(ScoreExperian(
                model_code=str(m.modelCode),
                score_value=m.scoreValue,
                model_date=m.modelDate,
            ))

    return ResultadoHDC(
        cedula=cedula,
        nombre_completo=nombre,
        obligaciones=obligaciones,
        obligaciones_cerradas=cerradas,
        scores=scores,
        huellas_consulta=len(report.inquiryFootprints),
        fecha_consulta=report.productResult.consultDate,
        codigo_respuesta=report.productResult.responseCode,
        mensaje_respuesta=report.productResult.responseDesc or "",
        respuesta_original=raw,
    )
