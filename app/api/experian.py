from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.services.experian_hdc import consultar_hdc
from app.services.experian_valor_ingreso import consultar_valor_ingreso

router = APIRouter(prefix="/experian", tags=["Experian"])


class ConsultaExperianRequest(BaseModel):
    numero_documento: str
    primer_apellido: str
    tipo_documento: str = "CC"


@router.post("/hdc")
async def obtener_hdc(req: ConsultaExperianRequest):
    try:
        resultado = await consultar_hdc(
            numero_documento=req.numero_documento,
            primer_apellido=req.primer_apellido,
            tipo_documento=req.tipo_documento,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error consultando HDC+: {e}")

    if resultado.codigo_respuesta != 13:
        raise HTTPException(
            status_code=422,
            detail=f"Experian respondió código {resultado.codigo_respuesta}: "
                   f"{resultado.mensaje_respuesta}",
        )

    return resultado


@router.post("/valor-ingreso")
async def obtener_valor_ingreso(req: ConsultaExperianRequest):
    try:
        resultado = await consultar_valor_ingreso(
            numero_documento=req.numero_documento,
            tipo_documento=req.tipo_documento,
        )
    except Exception as e:
        raise HTTPException(
            status_code=502, detail=f"Error consultando Valor Ingreso: {e}"
        )

    if resultado.status != "ok":
        raise HTTPException(
            status_code=422,
            detail=f"Experian Valor Ingreso: {resultado.status_message}",
        )

    return resultado


@router.post("/consulta-completa")
async def consulta_completa(req: ConsultaExperianRequest):
    """Consulta HDC+ y Valor Ingreso en una sola llamada."""
    errores = []
    hdc_result = None
    vi_result = None

    try:
        hdc_result = await consultar_hdc(
            numero_documento=req.numero_documento,
            primer_apellido=req.primer_apellido,
            tipo_documento=req.tipo_documento,
        )
    except Exception as e:
        errores.append(f"HDC+: {e}")

    try:
        vi_result = await consultar_valor_ingreso(
            numero_documento=req.numero_documento,
            tipo_documento=req.tipo_documento,
        )
    except Exception as e:
        errores.append(f"Valor Ingreso: {e}")

    if not hdc_result and not vi_result:
        raise HTTPException(
            status_code=502,
            detail=f"Ambas consultas fallaron: {'; '.join(errores)}",
        )

    return {
        "hdc": hdc_result,
        "valor_ingreso": vi_result,
        "errores": errores if errores else None,
    }
