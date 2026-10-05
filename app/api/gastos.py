from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.hdc import ObligacionCredito, ResultadoHDC
from app.models.gastos import AnalisisGastosResponse
from app.services.gastos import analizar_gastos, parametros_politica
from app.services.experian_hdc import consultar_hdc

router = APIRouter(prefix="/filtro", tags=["Filtro de Originación"])


@router.get("/parametros")
def endpoint_parametros():
    """Tablas de la política (gastos básicos y cuotas centrales) que usa el motor."""
    return parametros_politica()


class SolicitanteGastosInput(BaseModel):
    cedula: str = ""
    ingreso_bruto: float
    score_advance: Optional[int] = None
    obligaciones: List[ObligacionCredito] = []


class AnalisisGastosRequest(BaseModel):
    solicitante_principal: SolicitanteGastosInput
    solicitante_secundario: Optional[SolicitanteGastosInput] = None


@router.post("/analisis-gastos", response_model=AnalisisGastosResponse)
def endpoint_analisis_gastos(request: AnalisisGastosRequest):
    p = request.solicitante_principal
    s = request.solicitante_secundario

    return analizar_gastos(
        ingreso_bruto_principal=p.ingreso_bruto,
        cedula_principal=p.cedula,
        score_principal=p.score_advance,
        obligaciones_principal=p.obligaciones,
        ingreso_bruto_secundario=s.ingreso_bruto if s else 0,
        cedula_secundario=s.cedula if s else "",
        score_secundario=s.score_advance if s else None,
        obligaciones_secundario=s.obligaciones if s else None,
    )


class CapacidadPagoRequest(BaseModel):
    """Ingreso bruto por solicitante (ingreso calculado + arriendos).

    `retencion_fuente` y `solidaridad` son los que ya calculó el Análisis de
    Ingresos; si llegan, no se recalculan. Si no llegan, el motor los obtiene
    de las tablas de la política.
    """
    cedula: str
    primer_apellido: str
    tipo_documento: str = "CC"
    ingreso_bruto: float
    retencion_fuente: Optional[float] = None
    solidaridad: Optional[float] = None
    cedula_secundario: Optional[str] = None
    primer_apellido_secundario: Optional[str] = None
    tipo_documento_secundario: Optional[str] = None
    ingreso_bruto_secundario: Optional[float] = None
    retencion_fuente_secundario: Optional[float] = None
    solidaridad_secundario: Optional[float] = None


class CapacidadPagoResponse(BaseModel):
    hdc_principal: ResultadoHDC
    hdc_secundario: Optional[ResultadoHDC] = None
    analisis: AnalisisGastosResponse


@router.post("/capacidad-pago", response_model=CapacidadPagoResponse)
async def endpoint_capacidad_pago(request: CapacidadPagoRequest):
    try:
        hdc_principal = await consultar_hdc(
            numero_documento=request.cedula,
            primer_apellido=request.primer_apellido,
            tipo_documento=request.tipo_documento,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error consultando HDC: {e}")

    if hdc_principal.codigo_respuesta != 13:
        raise HTTPException(
            status_code=422,
            detail=f"HDC código {hdc_principal.codigo_respuesta}: "
                   f"{hdc_principal.mensaje_respuesta}",
        )

    hdc_secundario = None
    # El segundo solicitante se consulta siempre que venga identificado, para
    # conocer su score; sus egresos solo entran al cálculo si aporta ingreso.
    if request.cedula_secundario and request.primer_apellido_secundario:
        try:
            hdc_secundario = await consultar_hdc(
                numero_documento=request.cedula_secundario,
                primer_apellido=request.primer_apellido_secundario,
                tipo_documento=request.tipo_documento_secundario
                or request.tipo_documento,
            )
        except Exception as e:
            raise HTTPException(
                status_code=502, detail=f"Error consultando HDC secundario: {e}"
            )
        if hdc_secundario.codigo_respuesta != 13:
            raise HTTPException(
                status_code=422,
                detail=f"HDC secundario código {hdc_secundario.codigo_respuesta}: "
                       f"{hdc_secundario.mensaje_respuesta}",
            )

    analisis = analizar_gastos(
        ingreso_bruto_principal=request.ingreso_bruto,
        cedula_principal=request.cedula,
        score_principal=hdc_principal.score_advance,
        obligaciones_principal=hdc_principal.obligaciones,
        ingreso_bruto_secundario=request.ingreso_bruto_secundario or 0,
        cedula_secundario=request.cedula_secundario or "",
        score_secundario=hdc_secundario.score_advance if hdc_secundario else None,
        obligaciones_secundario=hdc_secundario.obligaciones if hdc_secundario else None,
        retefuente_principal=request.retencion_fuente,
        solidaridad_principal=request.solidaridad,
        retefuente_secundario=request.retencion_fuente_secundario,
        solidaridad_secundario=request.solidaridad_secundario,
    )

    return CapacidadPagoResponse(
        hdc_principal=hdc_principal,
        hdc_secundario=hdc_secundario,
        analisis=analisis,
    )
