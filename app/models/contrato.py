from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class NivelConfianza(str, Enum):
    ALTO = "alto"
    MEDIO = "medio"
    BAJO = "bajo"


class CampoExtraido(BaseModel):
    valor: Optional[str] = None
    confianza: float = 0.0
    fuente: str = ""
    requiere_revision: bool = False
    raw_text: Optional[str] = None
    pagina: Optional[int] = None


class CampoNumerico(CampoExtraido):
    valor_numerico: Optional[int] = None


class CampoBooleano(CampoExtraido):
    valor_bool: Optional[bool] = None


class DatosParteContrato(BaseModel):
    nombre: CampoExtraido = CampoExtraido()
    cedula: CampoExtraido = CampoExtraido()
    email: CampoExtraido = CampoExtraido()
    celular: CampoExtraido = CampoExtraido()
    ciudad: CampoExtraido = CampoExtraido()
    direccion_notificacion: CampoExtraido = CampoExtraido()


class ServiciosPublicos(BaseModel):
    agua: CampoBooleano = CampoBooleano()
    gas: CampoBooleano = CampoBooleano()
    energia: CampoBooleano = CampoBooleano()
    telefono: CampoBooleano = CampoBooleano()
    internet: CampoBooleano = CampoBooleano()


class DatosInmueble(BaseModel):
    direccion: CampoExtraido = CampoExtraido()
    barrio: CampoExtraido = CampoExtraido()
    ciudad: CampoExtraido = CampoExtraido()
    propiedad_horizontal: CampoBooleano = CampoBooleano()
    servicios: ServiciosPublicos = ServiciosPublicos()


class DatosFinancieros(BaseModel):
    canon_mensual: CampoNumerico = CampoNumerico()
    canon_letras: CampoExtraido = CampoExtraido()
    canon_cruce_ok: Optional[bool] = None
    admin_incluida: CampoBooleano = CampoBooleano()
    nombre_propietario_cuenta: CampoExtraido = CampoExtraido()
    tipo_cuenta: CampoExtraido = CampoExtraido()
    numero_cuenta: CampoExtraido = CampoExtraido()
    banco: CampoExtraido = CampoExtraido()


class DatosVigencia(BaseModel):
    fecha_inicio: CampoExtraido = CampoExtraido()
    fecha_terminacion: CampoExtraido = CampoExtraido()
    vigencia_meses: CampoNumerico = CampoNumerico()
    vigencia_cruce_ok: Optional[bool] = None


class VerificacionFirma(BaseModel):
    tiene_firma_arrendador: bool = False
    tiene_firma_arrendatario: bool = False
    confianza_arrendador: float = 0.0
    confianza_arrendatario: float = 0.0
    ambas_firmadas: bool = False


class ResumenContrato(BaseModel):
    """Los datos clave que se verifican del contrato de arrendamiento."""
    nombre_arrendador: CampoExtraido = CampoExtraido()
    cedula_arrendador: CampoExtraido = CampoExtraido()
    canon_mensual: CampoNumerico = CampoNumerico()
    fecha_inicio: CampoExtraido = CampoExtraido()
    firma: VerificacionFirma = VerificacionFirma()
    motor_principal: str = ""
    tiempo_procesamiento_ms: int = 0


class ContratoExtraido(BaseModel):
    arrendador: DatosParteContrato = DatosParteContrato()
    arrendatario: DatosParteContrato = DatosParteContrato()
    inmueble: DatosInmueble = DatosInmueble()
    financiero: DatosFinancieros = DatosFinancieros()
    vigencia: DatosVigencia = DatosVigencia()
    firma: VerificacionFirma = VerificacionFirma()

    confianza_global: float = 0.0
    nivel: NivelConfianza = NivelConfianza.BAJO
    campos_revision: list[str] = []
    validaciones_fallidas: list[str] = []
    motor_principal: str = ""
    tiempo_procesamiento_ms: int = 0
    texto_completo: str = ""

    def resumen(self) -> ResumenContrato:
        return ResumenContrato(
            nombre_arrendador=self.arrendador.nombre,
            cedula_arrendador=self.arrendador.cedula,
            canon_mensual=self.financiero.canon_mensual,
            fecha_inicio=self.vigencia.fecha_inicio,
            firma=self.firma,
            motor_principal=self.motor_principal,
            tiempo_procesamiento_ms=self.tiempo_procesamiento_ms,
        )
