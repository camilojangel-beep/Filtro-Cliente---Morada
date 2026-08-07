import uuid
from datetime import datetime, timezone, timedelta

import httpx

from app.config import settings
from app.services.experian_auth import obtener_token_hdc
from app.models.hdc import (
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


def _procesar_respuesta(raw: dict, cedula: str) -> ResultadoHDC:
    hdc = HDCplusResponse.model_validate(raw)
    report = hdc.ReportHDCplus

    if report.productResult.responseCode != 13:
        return ResultadoHDC(
            cedula=cedula,
            codigo_respuesta=report.productResult.responseCode,
            mensaje_respuesta=report.productResult.responseDesc or "",
        )

    nombre = ""
    if report.basicInformation:
        bi = report.basicInformation
        partes = [bi.names or "", bi.firstLastName or "", bi.secondLastName or ""]
        nombre = " ".join(p for p in partes if p).strip()

    obligaciones = []
    for entry in report.savings:
        acct = entry.account
        if acct.accountType is None:
            continue

        # Solo cuentas de crédito, no de ahorro/corriente
        if acct.accountType in (1, 51):
            continue

        linea = clasificar_linea_credito(
            acct.accountType,
            acct.subAccountType or "00",
        )

        cupo = acct.creditLimit or acct.disbursementAmount or 0
        saldo = acct.currentBalance or 0
        cuota = acct.installmentAmount or 0

        obligaciones.append(ObligacionCredito(
            entidad_nit=acct.counterpartyIdNumber or "",
            entidad_nombre=acct.businessLineName or "",
            linea_credito=linea,
            account_type=acct.accountType,
            sub_account_type=acct.subAccountType or "00",
            sub_account_type_desc=acct.subAccountTypeDesc or "",
            cupo=cupo,
            saldo=saldo,
            cuota_reportada=cuota,
            fecha_apertura=acct.accountOpeningDate,
            fecha_vencimiento=acct.accountExpirationDate,
            fecha_corte=acct.behaviourDate or (
                entry.status.behaviourDate if entry.status else None
            ),
            calidad_deudor=acct.guarantorCode or "00",
            periodicidad=acct.paymentPeriodicity or 1,
            cuotas_restantes=acct.remainingInstallments,
            cuotas_mora=acct.pastDueInstallments or 0,
            monto_mora=acct.pastDueAmount or 0,
        ))

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
        scores=scores,
        huellas_consulta=len(report.inquiryFootprints),
        fecha_consulta=report.productResult.consultDate,
        codigo_respuesta=report.productResult.responseCode,
        mensaje_respuesta=report.productResult.responseDesc or "",
    )
