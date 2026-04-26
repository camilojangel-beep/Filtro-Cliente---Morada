from enum import Enum
from pydantic import BaseModel
from typing import List, Optional

from app.models.experian import ExperianResponse


class Parentesco(str, Enum):
    CONYUGE = "conyuge"
    COMPANERO_PERMANENTE = "companero_permanente"
    PADRE = "padre"
    HIJO = "hijo"
    ABUELO = "abuelo"
    NIETO = "nieto"
    HERMANO = "hermano"
    SUEGRO = "suegro"
    HIJASTRO = "hijastro"
    YERNO_NUERA = "yerno_nuera"
    HIJO_ADOPTIVO = "hijo_adoptivo"
    PADRE_ADOPTIVO = "padre_adoptivo"


class EmpleadorFlag(BaseModel):
    nit: str
    marca_inconsistencia: bool = False


class IngresoArriendoInput(BaseModel):
    pin_certificado: str
    fecha_emision_certificado: str
    propietario_cedula: str
    ingreso_arriendo_declarado: float
    valor_arriendo_simulador: Optional[float] = None
    valor_inmueble_simulador: Optional[float] = None
    meses_contrato: Optional[int] = None


class EvaluarIngresoRequest(BaseModel):
    solicitante_principal: ExperianResponse
    solicitante_secundario: Optional[ExperianResponse] = None
    parentesco: Optional[Parentesco] = None
    score_principal: float
    score_secundario: Optional[float] = None
    moras_actuales_secundario: Optional[float] = None
    flags_empleadores: Optional[List[EmpleadorFlag]] = None
    arriendos_principal: Optional[List[IngresoArriendoInput]] = None
    arriendos_secundario: Optional[List[IngresoArriendoInput]] = None


class VectorEntry(BaseModel):
    anio: int
    mes: int
    realizo_pago: bool
    ingresos: float


class DetalleIngresoArriendo(BaseModel):
    ingreso_aceptado: float
    ingreso_declarado: float
    valor_referencia: float
    metodo_referencia: str
    validaciones: List[str]
    observaciones: List[str]


class DetalleIngreso(BaseModel):
    ingreso_calculado: float
    decision_aplicada: str
    vector_consolidado: List[VectorEntry]
    observaciones: List[str]
    ingresos_arriendo: List[DetalleIngresoArriendo] = []
    total_ingreso_arriendo: float = 0.0
    ingreso_bruto: float = 0.0


class EvaluarIngresoResponse(BaseModel):
    solicitante_principal: DetalleIngreso
    solicitante_secundario: Optional[DetalleIngreso] = None
    ingreso_total: float
    segundo_solicitante_aceptado: Optional[bool] = None
    observaciones_generales: List[str]
