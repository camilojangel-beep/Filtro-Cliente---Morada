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
    fila_tabla_meses: Optional[int] = None   # fila usada en las tablas % saldo / % contingente
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
    calidad_deudor_desc: str = ""
    es_deudor_principal: bool
    porcentaje_calidad: float
    cuota_ajustada_calidad: float
    cuotas_restantes: Optional[int] = None
    excluida_por_cuotas: bool = False
    cuota_final: float

    # Estado y mora (desde HDC+)
    estado_cuenta: str = ""
    estado_cuenta_desc: str = ""
    cuotas_mora: int = 0
    monto_mora: float = 0
    en_mora: bool = False
    castigada: bool = False

    observaciones: List[str] = []


class AnalisisGastosSolicitante(BaseModel):
    cedula: str
    # 8.3: ingreso calculado en el Análisis de Ingresos + arriendos que cuentan
    ingreso_bruto: float
    ingreso_smlmv: float
    score_advance: Optional[int] = None
    nivel_riesgo: int

    # 8.4: porcentaje buscado con el ingreso bruto y aplicado al ingreso bruto
    fila_tabla_gastos: int = 6   # fila usada en la tabla de gastos básicos (rango SMLMV)
    porcentaje_gastos_basicos: float
    gastos_basicos: float

    # 8.5
    detalle_obligaciones: List[DetalleObligacion] = []
    total_cuotas_centrales: float
    obligaciones_en_mora: int = 0
    obligaciones_castigadas: int = 0
    monto_mora_total: float = 0
    saldo_castigado: float = 0

    # 8.6. Si `descuentos_del_analisis_ingresos` es True, retención en la
    # fuente y fondo de solidaridad son los que calculó el Análisis de
    # Ingresos; si no, salen de las tablas de la política.
    descuentos_del_analisis_ingresos: bool = False
    porcentaje_retefuente: float
    retefuente: float
    porcentaje_solidaridad: float
    solidaridad: float
    total_descuentos_nomina: float

    # Ingreso bruto - retención en la fuente - fondo de solidaridad - gastos básicos
    ingreso_neto_calculado: float = 0

    total_egresos_solicitante: float


class AnalisisGastosResponse(BaseModel):
    solicitante_principal: AnalisisGastosSolicitante
    solicitante_secundario: Optional[AnalisisGastosSolicitante] = None

    # 8.3
    total_ingreso_bruto: float

    # Suma del Ingreso Neto Calculado de los solicitantes
    total_ingreso_neto_calculado: float = 0

    # 8.7
    total_egresos: float

    # 8.8 = Ingreso Neto Calculado - cuotas en centrales
    ingreso_neto: float

    # 8.9
    factor_ajuste: float
    nivel_riesgo_ajuste: int

    # 8.10
    disponible_pago: float
