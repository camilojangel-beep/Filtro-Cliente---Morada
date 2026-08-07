from pydantic import BaseModel
from typing import List, Optional

from app.models.hdc import LineaCredito


class DetalleObligacion(BaseModel):
    entidad: str
    linea_credito: LineaCredito
    cupo: float
    saldo: float
    cuota_reportada: float

    cuota_anualidad: Optional[float] = None

    # TDC/ROT: desglose saldo + cupo contingente
    meses_para_pagar: Optional[float] = None
    porcentaje_saldo: Optional[float] = None
    cuota_por_saldo: Optional[float] = None
    cupo_contingente: Optional[float] = None
    porcentaje_contingente: Optional[float] = None
    cuota_por_contingente: Optional[float] = None

    # CAB/VIV: desglose por fechas
    meses_faltantes: Optional[float] = None
    plazo_total_meses: Optional[float] = None

    base_calculo: float
    cuota_calculada: float
    calidad_deudor: str
    es_deudor_principal: bool
    porcentaje_calidad: float
    cuota_ajustada_calidad: float
    cuotas_restantes: Optional[int] = None
    excluida_por_cuotas: bool = False
    cuota_final: float
    observaciones: List[str] = []


class AnalisisGastosSolicitante(BaseModel):
    cedula: str
    ingreso_bruto: float
    ingreso_smlmv: float
    score_advance: Optional[int] = None
    nivel_riesgo: int

    # 8.4
    porcentaje_gastos_basicos: float
    gastos_basicos: float

    # 8.5
    detalle_obligaciones: List[DetalleObligacion] = []
    total_cuotas_centrales: float

    # 8.6
    porcentaje_retefuente: float
    retefuente: float
    porcentaje_solidaridad: float
    solidaridad: float
    total_descuentos_nomina: float

    total_egresos_solicitante: float


class AnalisisGastosResponse(BaseModel):
    solicitante_principal: AnalisisGastosSolicitante
    solicitante_secundario: Optional[AnalisisGastosSolicitante] = None

    # 8.3
    total_ingreso_bruto: float

    # 8.7
    total_egresos: float

    # 8.8
    ingreso_neto: float

    # 8.9
    factor_ajuste: float
    nivel_riesgo_ajuste: int

    # 8.10
    disponible_pago: float
