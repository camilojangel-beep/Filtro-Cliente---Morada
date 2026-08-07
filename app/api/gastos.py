from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.hdc import ObligacionCredito, ResultadoHDC
from app.models.gastos import AnalisisGastosResponse
from app.services.gastos import analizar_gastos
from app.services.experian_hdc import consultar_hdc

router = APIRouter(prefix="/filtro", tags=["Filtro de Originación"])


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
    cedula: str
    primer_apellido: str
    tipo_documento: str = "CC"
    ingreso_bruto: float
    cedula_secundario: Optional[str] = None
    primer_apellido_secundario: Optional[str] = None
    ingreso_bruto_secundario: Optional[float] = None


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
    if (
        request.cedula_secundario
        and request.primer_apellido_secundario
        and request.ingreso_bruto_secundario
    ):
        try:
            hdc_secundario = await consultar_hdc(
                numero_documento=request.cedula_secundario,
                primer_apellido=request.primer_apellido_secundario,
                tipo_documento=request.tipo_documento,
            )
        except Exception as e:
            raise HTTPException(
                status_code=502, detail=f"Error consultando HDC secundario: {e}"
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
    )

    return CapacidadPagoResponse(
        hdc_principal=hdc_principal,
        hdc_secundario=hdc_secundario,
        analisis=analisis,
    )
