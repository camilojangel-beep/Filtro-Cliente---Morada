from datetime import date, datetime
from typing import List, Tuple, Optional

from app.models.experian import ExperianResponse, Aportante, ResultadoPago
from app.models.solicitud import (
    EvaluarIngresoRequest,
    EvaluarIngresoResponse,
    DetalleIngreso,
    VectorEntry,
    EmpleadorFlag,
    IngresoArriendoInput,
)
from app.services.otros_ingresos import calcular_ingresos_arriendos
from app.config import settings


class VectorPago:
    def __init__(self, anio: int, mes: int, realizo_pago: bool, ingresos: float):
        self.anio = anio
        self.mes = mes
        self.realizo_pago = realizo_pago
        self.ingresos = ingresos


# ---------------------------------------------------------------------------
# 8.1.1 — Construcción del vector de pagos
# ---------------------------------------------------------------------------


def parsear_fecha_consulta(fecha: str) -> datetime:
    return datetime.strptime(fecha, "%m/%d/%Y %I:%M:%S %p")


def determinar_inicio_vector(vector: List[VectorPago], dia_consulta: int) -> int:
    """
    Mes 0 (el más reciente del vector) es válido si:
      - La consulta se hace del día 20 en adelante, O
      - Es anterior al día 20 pero el mes 0 tiene ingreso > 0
    De lo contrario se empieza desde el índice 1 (mes -1).
    """
    if not vector:
        return 0

    if dia_consulta >= 20:
        return 0

    if vector[0].ingresos > 0:
        return 0

    return 1


# ---------------------------------------------------------------------------
# 8.1.4 — Consolidación de múltiples empleadores en un solo vector
# ---------------------------------------------------------------------------


def _es_independiente(cedula: str, nit_empleador: str) -> bool:
    return cedula.strip() == nit_empleador.strip()


def _tiene_marca_inconsistencia(
    nit: str, flags: Optional[List[EmpleadorFlag]]
) -> bool:
    if not flags:
        return False
    for f in flags:
        if f.nit.strip() == nit.strip() and f.marca_inconsistencia:
            return True
    return False


def consolidar_vector(
    aportantes: List[Aportante],
    cedula: str,
    flags_empleadores: Optional[List[EmpleadorFlag]] = None,
) -> Tuple[List[VectorPago], List[str], bool]:
    """
    Retorna (vector_consolidado, observaciones, tiene_bloqueo).
    tiene_bloqueo = True cuando cualquier condición fuerza ingreso 0.
    """
    observaciones: List[str] = []

    # --- Filtrar independientes (cédula == NIT) ---
    aportantes_validos: List[Aportante] = []
    for ap in aportantes:
        if _es_independiente(cedula, ap.numero_identificacion_aportante):
            observaciones.append(
                f"Aportante {ap.razon_social_aportante}: excluido "
                f"(independiente — cédula igual al NIT)"
            )
            continue
        aportantes_validos.append(ap)

    if not aportantes_validos:
        return [], observaciones, True

    # --- Verificar bloqueos globales ---
    hay_multiples = len(aportantes_validos) > 1

    # Licencia no remunerada en cualquier aportante → bloqueo
    for ap in aportantes_validos:
        if ap.tiene_licencia_no_remunerada_actualmente_empleador:
            observaciones.append(
                f"Aportante {ap.razon_social_aportante}: licencia no remunerada"
            )
            return [], observaciones, True

    # Marca de inconsistencia en cualquier empleador → bloqueo
    for ap in aportantes_validos:
        if _tiene_marca_inconsistencia(
            ap.numero_identificacion_aportante, flags_empleadores
        ):
            observaciones.append(
                f"Aportante {ap.razon_social_aportante}: marca de inconsistencia"
            )
            return [], observaciones, True

    # Novedad de retiro en TODOS los aportantes → bloqueo
    if all(ap.tiene_novedad_retiro_actualmente_empleado for ap in aportantes_validos):
        observaciones.append("Todos los aportantes tienen novedad de retiro")
        return [], observaciones, True

    # --- Construir vectores por aportante y consolidar ---
    pagos_por_periodo: dict[Tuple[int, int], dict] = {}

    for ap in aportantes_validos:
        pagos = sorted(
            ap.resultado_pagos,
            key=lambda p: (p.ano_periodo_validado, p.mes_periodo_validado),
            reverse=True,
        )

        # 8.1.4: si tiene retiro y hay otros aportantes, ignorar el más reciente
        if ap.tiene_novedad_retiro_actualmente_empleado and hay_multiples and pagos:
            observaciones.append(
                f"Aportante {ap.razon_social_aportante}: novedad de retiro, "
                f"se ignora el periodo más reciente"
            )
            pagos = pagos[1:]

        for pago in pagos:
            key = (pago.ano_periodo_validado, pago.mes_periodo_validado)
            if key not in pagos_por_periodo:
                pagos_por_periodo[key] = {"ingresos": 0.0, "realizo_pago": False}
            pagos_por_periodo[key]["ingresos"] += pago.ingresos
            if pago.realizo_pago:
                pagos_por_periodo[key]["realizo_pago"] = True

    vector = [
        VectorPago(
            anio=anio,
            mes=mes,
            realizo_pago=datos["realizo_pago"],
            ingresos=datos["ingresos"],
        )
        for (anio, mes), datos in sorted(
            pagos_por_periodo.items(), reverse=True
        )
    ]

    return vector, observaciones, False


# ---------------------------------------------------------------------------
# 8.1.2 — Tabla de decisiones para definir el ingreso
# ---------------------------------------------------------------------------


def aplicar_tabla_decisiones(
    vector: List[VectorPago], inicio: int
) -> Tuple[float, str]:
    """
    Aplica la tabla de decisiones sobre los 3 meses más recientes del vector
    (a partir de `inicio`).
    Retorna (ingreso_calculado, descripcion_decision).
    """
    if not vector or inicio >= len(vector):
        return 0.0, "Ingreso 0: vector de pagos vacío o insuficiente"

    # Meses -1, -2, -3 relativos al inicio válido del vector
    mes_1 = vector[inicio] if inicio < len(vector) else None
    mes_2 = vector[inicio + 1] if inicio + 1 < len(vector) else None
    mes_3 = vector[inicio + 2] if inicio + 2 < len(vector) else None

    pago_1 = mes_1.realizo_pago if mes_1 else False  # más reciente
    pago_2 = mes_2.realizo_pago if mes_2 else False
    pago_3 = mes_3.realizo_pago if mes_3 else False

    ingreso_1 = mes_1.ingresos if mes_1 else 0.0
    ingreso_2 = mes_2.ingresos if mes_2 else 0.0
    ingreso_3 = mes_3.ingresos if mes_3 else 0.0

    # Conteo de pagos en últimos 6 y 12 meses
    rango_6 = vector[inicio: inicio + 6]
    rango_12 = vector[inicio: inicio + 12]
    pagos_en_6 = sum(1 for v in rango_6 if v.realizo_pago)
    pagos_en_12 = sum(1 for v in rango_12 if v.realizo_pago)

    # --- Fila 5: Mes -1 sin pago → Ingreso 0 ---
    if not pago_1:
        return 0.0, "Ingreso 0: sin pago en el mes más reciente del vector"

    # --- Fila 1: SI SI SI → Promedio de 3 meses ---
    if pago_2 and pago_3:
        promedio = (ingreso_1 + ingreso_2 + ingreso_3) / 3
        return promedio, "Promedio de ingreso de los últimos 3 meses"

    # --- Filas 2 y 3: un mes sin pago de los dos anteriores ---
    if pago_3 and not pago_2:
        # SI(-3) NO(-2) SI(-1)
        if pagos_en_6 >= 5:
            promedio = (ingreso_1 + ingreso_3) / 2
            return (
                promedio,
                "Promedio de 2 meses con ingreso (≥5 pagos en últimos 6 meses)",
            )
        else:
            promedio = (ingreso_1 + 0.0 + ingreso_3) / 3
            return (
                promedio,
                "Promedio de 3 meses asumiendo mes sin pago como 0 "
                "(<5 pagos en últimos 6 meses)",
            )

    if pago_2 and not pago_3:
        # NO(-3) SI(-2) SI(-1)
        if pagos_en_6 >= 5:
            promedio = (ingreso_1 + ingreso_2) / 2
            return (
                promedio,
                "Promedio de 2 meses con ingreso (≥5 pagos en últimos 6 meses)",
            )
        else:
            promedio = (ingreso_1 + ingreso_2 + 0.0) / 3
            return (
                promedio,
                "Promedio de 3 meses asumiendo mes sin pago como 0 "
                "(<5 pagos en últimos 6 meses)",
            )

    # --- Fila 4: NO(-3) NO(-2) SI(-1) ---
    if not pago_2 and not pago_3:
        if pagos_en_12 >= 8:
            return (
                ingreso_1,
                "Último ingreso (≥8 pagos en últimos 12 meses)",
            )
        else:
            promedio = (ingreso_1 + 0.0 + 0.0) / 3
            return (
                promedio,
                "Promedio de 3 meses asumiendo meses sin pago como 0 "
                "(<8 pagos en últimos 12 meses)",
            )

    return 0.0, "Caso no contemplado en la tabla de decisiones"


# ---------------------------------------------------------------------------
# Cálculo de ingreso para un solo solicitante
# ---------------------------------------------------------------------------


def calcular_ingreso_solicitante(
    experian: ExperianResponse,
    flags_empleadores: Optional[List[EmpleadorFlag]] = None,
    arriendos: Optional[List[IngresoArriendoInput]] = None,
) -> DetalleIngreso:
    data = experian.data
    cedula = data.numero_identificacion_persona_natural
    fecha_consulta = parsear_fecha_consulta(data.fecha)

    # 8.1.4 — consolidar múltiples empleadores
    vector, observaciones, bloqueado = consolidar_vector(
        data.aportantes, cedula, flags_empleadores
    )

    if bloqueado or not vector:
        ingreso = 0.0
        decision = observaciones[-1] if observaciones else "Sin aportantes válidos"
        vector_entries = []
    else:
        # 8.1.1 — determinar inicio válido del vector
        inicio = determinar_inicio_vector(vector, fecha_consulta.day)
        # 8.1.2 — aplicar tabla de decisiones
        ingreso, decision = aplicar_tabla_decisiones(vector, inicio)
        vector_entries = [
            VectorEntry(
                anio=v.anio, mes=v.mes,
                realizo_pago=v.realizo_pago, ingresos=v.ingresos,
            )
            for v in vector
        ]

    # 8.2.1 — ingresos por arriendos
    total_arriendo, detalles_arriendo = calcular_ingresos_arriendos(
        arriendos or [], cedula, date.today()
    )

    ingreso_bruto = ingreso + total_arriendo

    return DetalleIngreso(
        ingreso_calculado=ingreso,
        decision_aplicada=decision,
        vector_consolidado=vector_entries,
        observaciones=observaciones,
        ingresos_arriendo=detalles_arriendo,
        total_ingreso_arriendo=total_arriendo,
        ingreso_bruto=ingreso_bruto,
    )


# ---------------------------------------------------------------------------
# 8.1.3 — Evaluación con dos solicitantes
# ---------------------------------------------------------------------------


def _validar_segundo_solicitante(
    ingreso_principal: float,
    ingreso_secundario: float,
    score_secundario: Optional[float],
    moras_actuales_secundario: Optional[float],
) -> Tuple[bool, str]:
    """
    Valida si el segundo solicitante puede sumar su ingreso.
    Retorna (aceptado, motivo).
    """
    ingreso_total = ingreso_principal + ingreso_secundario

    if ingreso_total == 0:
        return False, "Ingreso total es cero, no se puede evaluar participación"

    participacion = ingreso_secundario / ingreso_total

    if participacion > settings.PARTICIPACION_MINIMA_SEGUNDO_SOLICITANTE:
        score_minimo = settings.SCORE_MINIMO_PRODUCTO
        if score_secundario is None or score_secundario < score_minimo:
            return False, (
                f"Participación del segundo solicitante ({participacion:.1%}) > 20%: "
                f"requiere score ≥ {score_minimo}, "
                f"tiene {score_secundario}"
            )
    else:
        mora_maxima = settings.MORA_MAXIMA_SEGUNDO_SOLICITANTE_SMLMV * settings.SMLMV
        moras = moras_actuales_secundario or 0.0
        if moras > mora_maxima:
            return False, (
                f"Participación del segundo solicitante ({participacion:.1%}) ≤ 20%: "
                f"moras actuales (${moras:,.0f}) superan el máximo "
                f"permitido (${mora_maxima:,.0f} = 0.5 SMLMV)"
            )

    return True, "Segundo solicitante aceptado"


# ---------------------------------------------------------------------------
# Punto de entrada principal
# ---------------------------------------------------------------------------


def evaluar_ingreso(request: EvaluarIngresoRequest) -> EvaluarIngresoResponse:
    observaciones_generales: List[str] = []

    # --- Solicitante principal ---
    detalle_principal = calcular_ingreso_solicitante(
        request.solicitante_principal,
        request.flags_empleadores,
        request.arriendos_principal,
    )

    # --- Solicitante secundario (8.1.3) ---
    detalle_secundario: Optional[DetalleIngreso] = None
    segundo_aceptado: Optional[bool] = None
    ingreso_total = detalle_principal.ingreso_bruto

    if request.solicitante_secundario is not None:
        if request.parentesco is None:
            observaciones_generales.append(
                "Segundo solicitante rechazado: no se indicó parentesco"
            )
            segundo_aceptado = False
        else:
            detalle_secundario = calcular_ingreso_solicitante(
                request.solicitante_secundario,
                request.flags_empleadores,
                request.arriendos_secundario,
            )

            aceptado, motivo = _validar_segundo_solicitante(
                detalle_principal.ingreso_bruto,
                detalle_secundario.ingreso_bruto,
                request.score_secundario,
                request.moras_actuales_secundario,
            )
            segundo_aceptado = aceptado
            observaciones_generales.append(motivo)

            if aceptado:
                ingreso_total += detalle_secundario.ingreso_bruto

    return EvaluarIngresoResponse(
        solicitante_principal=detalle_principal,
        solicitante_secundario=detalle_secundario,
        ingreso_total=ingreso_total,
        segundo_solicitante_aceptado=segundo_aceptado,
        observaciones_generales=observaciones_generales,
    )
