from datetime import date, datetime
from typing import List, Tuple

from app.models.solicitud import IngresoArriendoInput, DetalleIngresoArriendo

PORCENTAJE_MAXIMO_ARRIENDO = 0.0055  # 0.55% mensual sobre valor del inmueble
VIGENCIA_CERTIFICADO_DIAS = 30
MESES_MINIMOS_CONTRATO = 4


def calcular_ingreso_arriendo(
    arriendo: IngresoArriendoInput,
    cedula_solicitante: str,
    fecha_evaluacion: date,
) -> DetalleIngresoArriendo:
    validaciones: List[str] = []
    observaciones: List[str] = []
    declarado = arriendo.ingreso_arriendo_declarado

    def _rechazar(motivo: str) -> DetalleIngresoArriendo:
        validaciones.append(motivo)
        return DetalleIngresoArriendo(
            ingreso_aceptado=0.0,
            ingreso_declarado=declarado,
            valor_referencia=0.0,
            metodo_referencia="N/A",
            validaciones=validaciones,
            observaciones=observaciones,
        )

    # --- 1. Vigencia del certificado (máx 30 días) ---
    try:
        fecha_emision = datetime.strptime(
            arriendo.fecha_emision_certificado, "%Y-%m-%d"
        ).date()
    except ValueError:
        return _rechazar(
            "RECHAZADO: Formato de fecha del certificado inválido (usar YYYY-MM-DD)"
        )

    dias = (fecha_evaluacion - fecha_emision).days
    if dias > VIGENCIA_CERTIFICADO_DIAS:
        return _rechazar(
            f"RECHAZADO: Certificado vencido ({dias} días, máximo {VIGENCIA_CERTIFICADO_DIAS})"
        )
    if dias < 0:
        return _rechazar("RECHAZADO: Fecha de emisión del certificado es futura")
    validaciones.append(f"Certificado vigente ({dias} días)")

    # --- 2. Propiedad coincide con solicitante ---
    if arriendo.propietario_cedula.strip() != cedula_solicitante.strip():
        return _rechazar(
            "RECHAZADO: Propietario del inmueble no coincide con el solicitante"
        )
    validaciones.append("Propiedad verificada (coincide con solicitante)")

    # --- 3. Contrato mínimo 4 meses ---
    if arriendo.meses_contrato < MESES_MINIMOS_CONTRATO:
        return _rechazar(
            f"RECHAZADO: Contrato con {arriendo.meses_contrato} meses "
            f"(mínimo {MESES_MINIMOS_CONTRATO})"
        )
    validaciones.append(f"Antigüedad del contrato: {arriendo.meses_contrato} meses")

    # --- 4. Valor de referencia ---
    valor_ref = 0.0
    metodo = ""

    tiene_sim_arriendo = arriendo.valor_arriendo_simulador is not None
    tiene_sim_inmueble = arriendo.valor_inmueble_simulador is not None

    if tiene_sim_arriendo and tiene_sim_inmueble:
        ref_simulador = arriendo.valor_arriendo_simulador
        ref_porcentaje = arriendo.valor_inmueble_simulador * PORCENTAJE_MAXIMO_ARRIENDO
        valor_ref = min(ref_simulador, ref_porcentaje)
        metodo = (
            f"Menor entre simulador de arriendo (${ref_simulador:,.0f}) "
            f"y 0.55% del valor del inmueble (${ref_porcentaje:,.0f})"
        )
    elif tiene_sim_arriendo:
        valor_ref = arriendo.valor_arriendo_simulador
        metodo = "Simulador de arriendo"
    elif tiene_sim_inmueble:
        valor_ref = arriendo.valor_inmueble_simulador * PORCENTAJE_MAXIMO_ARRIENDO
        metodo = (
            f"0.55% del valor del inmueble "
            f"(${arriendo.valor_inmueble_simulador:,.0f})"
        )
    else:
        return _rechazar(
            "RECHAZADO: No se proporcionó valor de referencia "
            "(simulador de arriendo o valor del inmueble)"
        )

    # --- 5. Ingreso = mín(declarado, referencia) ---
    ingreso_aceptado = min(declarado, valor_ref)

    if declarado > valor_ref:
        observaciones.append(
            f"Ingreso declarado (${declarado:,.0f}) supera la referencia "
            f"(${valor_ref:,.0f}): se toma el valor de referencia"
        )

    validaciones.append("Ingreso por arriendo aprobado")

    return DetalleIngresoArriendo(
        ingreso_aceptado=ingreso_aceptado,
        ingreso_declarado=declarado,
        valor_referencia=valor_ref,
        metodo_referencia=metodo,
        validaciones=validaciones,
        observaciones=observaciones,
    )


def calcular_ingresos_arriendos(
    arriendos: List[IngresoArriendoInput],
    cedula_solicitante: str,
    fecha_evaluacion: date,
) -> Tuple[float, List[DetalleIngresoArriendo]]:
    if not arriendos:
        return 0.0, []

    detalles: List[DetalleIngresoArriendo] = []
    total = 0.0

    for arriendo in arriendos:
        detalle = calcular_ingreso_arriendo(
            arriendo, cedula_solicitante, fecha_evaluacion
        )
        detalles.append(detalle)
        total += detalle.ingreso_aceptado

    return total, detalles
