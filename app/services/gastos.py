from datetime import datetime, date
from typing import List, Optional, Tuple

from app.config import settings
from app.models.hdc import LineaCredito, ObligacionCredito
from app.models.gastos import (
    AnalisisGastosSolicitante,
    AnalisisGastosResponse,
    DetalleObligacion,
)

# =========================================================================
# Tablas de parámetros (fuente: MORADA_Tablas_de_Gastos_básicos…xlsx)
# =========================================================================

# --- 8.4 Gastos básicos: porcentaje por nivel de ingreso × nivel de riesgo ---
_TABLA_GASTOS_BASICOS: list[Tuple[float, list[float]]] = [
    (15, [0.20, 0.25, 0.30, 0.30, 0.35, 0.35]),
    (10, [0.25, 0.30, 0.35, 0.35, 0.40, 0.40]),
    (8,  [0.30, 0.35, 0.40, 0.40, 0.45, 0.45]),
    (4,  [0.35, 0.40, 0.45, 0.45, 0.50, 0.50]),
    (2,  [0.40, 0.45, 0.50, 0.50, 0.55, 0.55]),
    (1,  [0.45, 0.50, 0.55, 0.55, 0.60, 0.60]),
    (0,  [0.75, 0.80, 0.85, 0.85, 0.90, 0.90]),
]

# --- 8.6a Retención en la fuente ---
_TABLA_RETEFUENTE: list[Tuple[float, float]] = [
    (24, 0.1513),
    (23, 0.1487),
    (22, 0.1458),
    (21, 0.1427),
    (20, 0.1393),
    (19, 0.1362),
    (18, 0.1327),
    (17, 0.1287),
    (16, 0.1242),
    (15, 0.1250),
    (14, 0.1210),
    (13, 0.1164),
    (12, 0.1112),
    (11, 0.1050),
    (10, 0.0978),
    (9,  0.0891),
    (8,  0.0784),
    (7,  0.0651),
    (6,  0.0481),
    (5,  0.0354),
    (4,  0.0174),
    (0,  0.0),
]

# --- 8.6b Fondo de solidaridad pensional ---
_TABLA_SOLIDARIDAD: list[Tuple[float, float]] = [
    (20, 0.020),
    (19, 0.018),
    (18, 0.016),
    (17, 0.014),
    (16, 0.012),
    (4,  0.010),
    (0,  0.0),
]

# --- 8.9 Factor de ajuste al ingreso neto ---
_TABLA_FACTOR_AJUSTE: list[Tuple[int, float]] = [
    (895, 1.00),
    (850, 0.95),
    (807, 0.90),
    (753, 0.85),
    (707, 0.80),
    (0,   0.75),
]

# --- Periodicidad → meses por periodo ---
_MESES_PERIODICIDAD: dict[int, int] = {
    0: 1, 1: 1, 2: 2, 3: 3, 4: 6, 5: 12, 6: 1, 9: 1,
}

# =========================================================================
# 8.5 — Parámetros para cálculo de cuotas de endeudamiento
#       (fuente: MORADA_CAPITAL_Cálculo_Cuotas_Endeudamiento…xlsx)
# =========================================================================

# Tasas EA y plazos fijos por tipo de crédito
_TASA_EA_TDC = 0.20
_PLAZO_TDC = 36
_TASA_EA_ROT = 0.25
_PLAZO_ROT = 60
_TASA_EA_CAB = 0.125
_TASA_EA_VIV = 0.11

# Porcentaje de cuota sobre SALDO de TDC/ROT por rango de meses × riesgo
# Cada fila: [R1, R2, R3, R4, R5, R6]
# Fila 0: meses == 0
# Fila 1: 0 < meses <= 3  ...  Fila 5: meses > 12
_TABLA_PCT_SALDO: list[list[float]] = [
    [0,    0,    0,    0,    0,    0   ],
    [0.15, 0.20, 0.25, 0.30, 0.35, 0.65],
    [0.25, 0.30, 0.35, 0.40, 0.50, 0.75],
    [0.45, 0.50, 0.55, 0.60, 0.70, 0.90],
    [0.60, 0.65, 0.70, 0.75, 0.85, 1.00],
    [0.75, 0.80, 0.85, 0.90, 1.00, 1.00],
]

# Porcentaje de cuota sobre CUPO CONTINGENTE de TDC/ROT
_TABLA_PCT_CONTINGENTE: list[list[float]] = [
    [0,    0.05, 0.10, 0.15, 0.20, 0.25],
    [0.05, 0.10, 0.15, 0.20, 0.25, 0.35],
    [0.15, 0.20, 0.25, 0.30, 0.35, 0.45],
    [0.35, 0.40, 0.45, 0.50, 0.55, 0.60],
    [0.50, 0.55, 0.60, 0.65, 0.70, 0.80],
    [0.65, 0.70, 0.75, 0.80, 0.85, 1.00],
]


# =========================================================================
# Funciones auxiliares
# =========================================================================

def _nivel_riesgo(score: Optional[int]) -> int:
    if score is None:
        return 6
    if score >= 895:
        return 1
    if score >= 850:
        return 2
    if score >= 807:
        return 3
    if score >= 753:
        return 4
    if score >= 707:
        return 5
    return 6


def _tasa_mensual(tasa_ea: float) -> float:
    return (1 + tasa_ea) ** (1 / 12) - 1


def _pmt(tasa_mensual: float, n_meses: float, valor_presente: float) -> float:
    if tasa_mensual <= 0 or n_meses <= 0 or valor_presente <= 0:
        return 0.0
    factor = (1 + tasa_mensual) ** n_meses
    return valor_presente * tasa_mensual * factor / (factor - 1)


def _buscar_pct(tabla: list[list[float]], meses: float, nivel_riesgo: int) -> float:
    idx = nivel_riesgo - 1
    if meses == 0:
        return tabla[0][idx]
    if meses <= 3:
        return tabla[1][idx]
    if meses <= 6:
        return tabla[2][idx]
    if meses <= 9:
        return tabla[3][idx]
    if meses <= 12:
        return tabla[4][idx]
    return tabla[5][idx]


def _parse_fecha(fecha_str: Optional[str]) -> Optional[date]:
    if not fecha_str:
        return None
    try:
        s = fecha_str.split("T")[0] if "T" in fecha_str else fecha_str
        return datetime.strptime(s, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def _meses_entre_fechas(
    fecha_inicio_str: Optional[str], fecha_fin_str: Optional[str]
) -> Optional[float]:
    inicio = _parse_fecha(fecha_inicio_str)
    fin = _parse_fecha(fecha_fin_str)
    if not inicio or not fin:
        return None
    dias = (fin - inicio).days
    if dias <= 0:
        return 0.0
    return dias * 12 / 365


def _es_deudor_principal(calidad: str) -> bool:
    return calidad == "00"


def _porcentaje_calidad(calidad: str, linea: LineaCredito) -> float:
    if _es_deudor_principal(calidad):
        return 1.0
    if linea in (LineaCredito.TDC, LineaCredito.ROT, LineaCredito.SOSTENIMIENTO):
        return 1.0
    if linea == LineaCredito.VIV:
        return 0.50
    return 0.25


def _cuota_mensual_equivalente(cuota: float, periodicidad: int) -> float:
    meses = _MESES_PERIODICIDAD.get(periodicidad, 1)
    if meses <= 0:
        meses = 1
    return cuota / meses


# =========================================================================
# 8.4 — Gastos básicos
# =========================================================================

def calcular_gastos_basicos(
    ingreso_bruto: float, score: Optional[int]
) -> Tuple[float, float]:
    smlmv = settings.SMLMV
    n = ingreso_bruto / smlmv if smlmv else 0
    idx = _nivel_riesgo(score) - 1

    if n > 15:
        porcentajes = _TABLA_GASTOS_BASICOS[0][1]
    elif n > 10:
        porcentajes = _TABLA_GASTOS_BASICOS[1][1]
    elif n > 8:
        porcentajes = _TABLA_GASTOS_BASICOS[2][1]
    elif n > 4:
        porcentajes = _TABLA_GASTOS_BASICOS[3][1]
    elif n > 2:
        porcentajes = _TABLA_GASTOS_BASICOS[4][1]
    elif n >= 1:
        porcentajes = _TABLA_GASTOS_BASICOS[5][1]
    else:
        porcentajes = _TABLA_GASTOS_BASICOS[6][1]

    pct = porcentajes[idx]
    return pct, ingreso_bruto * pct


# =========================================================================
# 8.5 — Cuotas centrales de riesgo
# =========================================================================

def _calcular_cuota_tdc_rot(
    ob: ObligacionCredito, nivel: int, obs: list[str],
) -> DetalleObligacion:
    if ob.linea_credito == LineaCredito.TDC:
        tasa_ea, plazo = _TASA_EA_TDC, _PLAZO_TDC
    else:
        tasa_ea, plazo = _TASA_EA_ROT, _PLAZO_ROT

    tasa_m = _tasa_mensual(tasa_ea)

    # --- Cuota por saldo ---
    cuota_anualidad_saldo = _pmt(tasa_m, plazo, ob.saldo)
    max_cuota = max(ob.cuota_reportada, cuota_anualidad_saldo)
    meses_pagar = ob.saldo / max_cuota if max_cuota > 0 else 0.0

    pct_saldo = _buscar_pct(_TABLA_PCT_SALDO, meses_pagar, nivel)
    cuota_saldo = max_cuota * pct_saldo

    # --- Cuota por cupo contingente ---
    cupo_cont = max(0.0, ob.cupo - ob.saldo)
    cuota_anualidad_cont = _pmt(tasa_m, plazo, cupo_cont)
    pct_cont = _buscar_pct(_TABLA_PCT_CONTINGENTE, meses_pagar, nivel)
    cuota_cont = cuota_anualidad_cont * pct_cont

    cuota_total = cuota_saldo + cuota_cont

    return DetalleObligacion(
        entidad=ob.entidad_nombre,
        linea_credito=ob.linea_credito,
        cupo=ob.cupo,
        saldo=ob.saldo,
        cuota_reportada=ob.cuota_reportada,
        cuota_anualidad=round(cuota_anualidad_saldo, 2),
        meses_para_pagar=round(meses_pagar, 2),
        porcentaje_saldo=pct_saldo,
        cuota_por_saldo=round(cuota_saldo, 2),
        cupo_contingente=round(cupo_cont, 2),
        porcentaje_contingente=pct_cont,
        cuota_por_contingente=round(cuota_cont, 2),
        base_calculo=ob.saldo,
        cuota_calculada=round(cuota_total, 2),
        calidad_deudor=ob.calidad_deudor,
        es_deudor_principal=_es_deudor_principal(ob.calidad_deudor),
        porcentaje_calidad=1.0,
        cuota_ajustada_calidad=round(cuota_total, 2),
        cuota_final=round(cuota_total, 2),
        observaciones=obs,
    )


def _calcular_cuota_cab_viv(
    ob: ObligacionCredito, nivel: int, obs: list[str],
) -> DetalleObligacion:
    tasa_ea = _TASA_EA_VIV if ob.linea_credito == LineaCredito.VIV else _TASA_EA_CAB
    tasa_m = _tasa_mensual(tasa_ea)

    meses_faltantes = _meses_entre_fechas(ob.fecha_corte, ob.fecha_vencimiento)
    plazo_total = _meses_entre_fechas(ob.fecha_apertura, ob.fecha_vencimiento)

    cuota_mensualizada = _cuota_mensual_equivalente(
        ob.cuota_reportada, ob.periodicidad
    )

    max_valor = max(ob.saldo, ob.cupo)
    cuota_anualidad = 0.0
    if plazo_total and plazo_total > 0 and max_valor > 0:
        cuota_anualidad = _pmt(tasa_m, plazo_total, max_valor)

    cuota = max(cuota_mensualizada, cuota_anualidad)

    if cuota_anualidad > cuota_mensualizada > 0:
        obs.append(
            f"Cuota calculada ({cuota_anualidad:,.0f}) > reportada ({cuota_mensualizada:,.0f})"
        )

    # Ajuste por calidad del deudor (solo CAB/VIV)
    principal = _es_deudor_principal(ob.calidad_deudor)
    pct_calidad = _porcentaje_calidad(ob.calidad_deudor, ob.linea_credito)
    cuota_calidad = cuota * pct_calidad

    if not principal:
        obs.append(
            f"Calidad {ob.calidad_deudor}: se aplica {pct_calidad:.0%} de la cuota"
        )

    # Exclusión: <= 2 meses faltantes calculados desde fechas, o cuotas_restantes
    excluida = False
    if meses_faltantes is not None and meses_faltantes <= 2:
        excluida = True
        obs.append(f"≤ 2 meses faltantes ({meses_faltantes:.1f}): cuota = 0")
    elif (
        meses_faltantes is None
        and ob.cuotas_restantes is not None
        and ob.cuotas_restantes <= 2
    ):
        excluida = True
        obs.append(f"≤ 2 cuotas restantes ({ob.cuotas_restantes}): cuota = 0")

    cuota_final = 0.0 if excluida else cuota_calidad

    return DetalleObligacion(
        entidad=ob.entidad_nombre,
        linea_credito=ob.linea_credito,
        cupo=ob.cupo,
        saldo=ob.saldo,
        cuota_reportada=ob.cuota_reportada,
        cuota_anualidad=round(cuota_anualidad, 2),
        meses_faltantes=round(meses_faltantes, 2) if meses_faltantes is not None else None,
        plazo_total_meses=round(plazo_total, 2) if plazo_total is not None else None,
        base_calculo=max_valor,
        cuota_calculada=round(cuota, 2),
        calidad_deudor=ob.calidad_deudor,
        es_deudor_principal=principal,
        porcentaje_calidad=pct_calidad,
        cuota_ajustada_calidad=round(cuota_calidad, 2),
        cuotas_restantes=ob.cuotas_restantes,
        excluida_por_cuotas=excluida,
        cuota_final=round(cuota_final, 2),
        observaciones=obs,
    )


def calcular_cuota_obligacion(
    ob: ObligacionCredito, score: Optional[int] = None,
) -> DetalleObligacion:
    obs: list[str] = []
    nivel = _nivel_riesgo(score)

    if ob.linea_credito == LineaCredito.SOSTENIMIENTO:
        return DetalleObligacion(
            entidad=ob.entidad_nombre,
            linea_credito=ob.linea_credito,
            cupo=ob.cupo,
            saldo=ob.saldo,
            cuota_reportada=ob.cuota_reportada,
            base_calculo=0,
            cuota_calculada=0,
            calidad_deudor=ob.calidad_deudor,
            es_deudor_principal=_es_deudor_principal(ob.calidad_deudor),
            porcentaje_calidad=0,
            cuota_ajustada_calidad=0,
            cuota_final=0,
            observaciones=["Sostenimiento: cuota = 0 (incluido en gastos básicos)"],
        )

    if ob.linea_credito in (LineaCredito.TDC, LineaCredito.ROT):
        return _calcular_cuota_tdc_rot(ob, nivel, obs)

    return _calcular_cuota_cab_viv(ob, nivel, obs)


def calcular_cuotas_centrales(
    obligaciones: List[ObligacionCredito],
    score: Optional[int] = None,
) -> Tuple[List[DetalleObligacion], float]:
    detalles = [calcular_cuota_obligacion(ob, score) for ob in obligaciones]
    total = sum(d.cuota_final for d in detalles)
    return detalles, total


# =========================================================================
# 8.6 — Descuentos de nómina
# =========================================================================

def calcular_retefuente(ingreso_bruto: float) -> Tuple[float, float]:
    smlmv = settings.SMLMV
    ingreso_smlmv = ingreso_bruto / smlmv if smlmv else 0

    porcentaje = 0.0
    for limite, pct in _TABLA_RETEFUENTE:
        if ingreso_smlmv > limite:
            porcentaje = pct
            break

    return porcentaje, ingreso_bruto * porcentaje


def calcular_solidaridad(ingreso_bruto: float) -> Tuple[float, float]:
    smlmv = settings.SMLMV
    n = ingreso_bruto / smlmv if smlmv else 0

    if n > 20:
        pct = 0.020
    elif n > 19:
        pct = 0.018
    elif n > 18:
        pct = 0.016
    elif n > 17:
        pct = 0.014
    elif n > 16:
        pct = 0.012
    elif n >= 4:
        pct = 0.010
    else:
        pct = 0.0

    return pct, ingreso_bruto * pct


# =========================================================================
# 8.9 — Factor de ajuste
# =========================================================================

def calcular_factor_ajuste(score: Optional[int]) -> Tuple[float, int]:
    nivel = _nivel_riesgo(score)
    for score_min, factor in _TABLA_FACTOR_AJUSTE:
        if (score or 0) >= score_min:
            return factor, nivel
    return 0.75, 6


# =========================================================================
# Análisis completo por solicitante
# =========================================================================

def analizar_gastos_solicitante(
    cedula: str,
    ingreso_bruto: float,
    score: Optional[int],
    obligaciones: List[ObligacionCredito],
) -> AnalisisGastosSolicitante:
    smlmv = settings.SMLMV
    ingreso_smlmv = ingreso_bruto / smlmv if smlmv else 0
    nivel = _nivel_riesgo(score)

    pct_gastos, gastos_basicos = calcular_gastos_basicos(ingreso_bruto, score)
    detalles_ob, total_cuotas = calcular_cuotas_centrales(obligaciones, score)
    pct_ret, retefuente = calcular_retefuente(ingreso_bruto)
    pct_sol, solidaridad = calcular_solidaridad(ingreso_bruto)
    descuentos = retefuente + solidaridad
    total_egresos = gastos_basicos + total_cuotas + descuentos

    return AnalisisGastosSolicitante(
        cedula=cedula,
        ingreso_bruto=ingreso_bruto,
        ingreso_smlmv=round(ingreso_smlmv, 2),
        score_advance=score,
        nivel_riesgo=nivel,
        porcentaje_gastos_basicos=pct_gastos,
        gastos_basicos=round(gastos_basicos, 2),
        detalle_obligaciones=detalles_ob,
        total_cuotas_centrales=round(total_cuotas, 2),
        porcentaje_retefuente=pct_ret,
        retefuente=round(retefuente, 2),
        porcentaje_solidaridad=pct_sol,
        solidaridad=round(solidaridad, 2),
        total_descuentos_nomina=round(descuentos, 2),
        total_egresos_solicitante=round(total_egresos, 2),
    )


# =========================================================================
# Punto de entrada: análisis completo (uno o dos solicitantes)
# =========================================================================

def analizar_gastos(
    ingreso_bruto_principal: float,
    score_principal: Optional[int],
    obligaciones_principal: List[ObligacionCredito],
    cedula_principal: str = "",
    ingreso_bruto_secundario: float = 0,
    cedula_secundario: str = "",
    score_secundario: Optional[int] = None,
    obligaciones_secundario: Optional[List[ObligacionCredito]] = None,
) -> AnalisisGastosResponse:

    principal = analizar_gastos_solicitante(
        cedula=cedula_principal or "principal",
        ingreso_bruto=ingreso_bruto_principal,
        score=score_principal,
        obligaciones=obligaciones_principal,
    )

    secundario = None
    if ingreso_bruto_secundario > 0 and obligaciones_secundario is not None:
        secundario = analizar_gastos_solicitante(
            cedula=cedula_secundario or "secundario",
            ingreso_bruto=ingreso_bruto_secundario,
            score=score_secundario,
            obligaciones=obligaciones_secundario or [],
        )

    total_ingreso = ingreso_bruto_principal + ingreso_bruto_secundario
    total_egresos = principal.total_egresos_solicitante
    if secundario:
        total_egresos += secundario.total_egresos_solicitante
    ingreso_neto = total_ingreso - total_egresos
    factor, nivel_ajuste = calcular_factor_ajuste(score_principal)
    disponible = ingreso_neto * factor

    return AnalisisGastosResponse(
        solicitante_principal=principal,
        solicitante_secundario=secundario,
        total_ingreso_bruto=round(total_ingreso, 2),
        total_egresos=round(total_egresos, 2),
        ingreso_neto=round(ingreso_neto, 2),
        factor_ajuste=factor,
        nivel_riesgo_ajuste=nivel_ajuste,
        disponible_pago=round(disponible, 2),
    )
