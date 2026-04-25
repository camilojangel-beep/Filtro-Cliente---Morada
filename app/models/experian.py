from pydantic import BaseModel
from typing import List, Optional


class ResultadoPago(BaseModel):
    ano_periodo_validado: int
    mes_periodo_validado: int
    realizo_pago: bool
    ingresos: float


class Aportante(BaseModel):
    tipo_identificacion_aportante_id: int
    numero_identificacion_aportante: str
    razon_social_aportante: str
    tipo_cotizante_persona_natural: int
    descripcion_cotizante_persona_natural: str
    tiene_salario_integral_actualmente: bool = False
    tiene_salario_fijo_actualmente: bool = False
    tiene_salario_variable_actualmente: bool = False
    tiene_novedad_ingreso_actualmente_empleador: bool = False
    tiene_novedad_retiro_actualmente_empleado: bool = False
    tiene_licencia_no_remunerada_actualmente_empleador: bool = False
    ingreso_maximo_empleador: float = 0
    ingreso_minimo_empleador: float = 0
    promedio_ingresos: float = 0
    media_ingresos: float = 0
    tipo_planilla: str = ""
    description_tipo_planilla: str = ""
    actividad_aportante: str = ""
    descripcion_actividad_aportante: str = ""
    nivel_impacto_aportante: str = ""
    benef_upc: Optional[bool] = None
    ded_obl_ley: Optional[float] = None
    resultado_pagos: List[ResultadoPago] = []


class ExperianData(BaseModel):
    fecha: str
    consulta_id: Optional[str] = None
    respuesta_id: Optional[int] = None
    tipo_identificacion_persona_natural_id: Optional[int] = None
    numero_identificacion_persona_natural: str
    primer_nombre_persona_natural: Optional[str] = None
    segundo_nombre_persona_natural: Optional[str] = None
    primer_apellido_persona_natural: Optional[str] = None
    segundo_apellido_persona_natural: Optional[str] = None
    EPS: Optional[str] = None
    AFP: Optional[str] = None
    aportantes: List[Aportante] = []


class ExperianResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    status: str
    status_message: Optional[str] = None
    provider: Optional[str] = None
    data: ExperianData
