from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TipoIdentificacion(str, Enum):
    CC = "CC"
    CE = "CE"


class DatosPersona(BaseModel):
    primer_nombre: str
    primer_apellido: str
    tipo_identificacion: TipoIdentificacion
    numero_identificacion: str


class DatosBasicosCliente(BaseModel):
    primer_nombre: str
    primer_apellido: str
    tipo_identificacion: TipoIdentificacion
    numero_identificacion: str
    autorizacion_aceptada: bool
    segundo_solicitante: Optional[DatosPersona] = None
    parentesco: Optional[str] = None
