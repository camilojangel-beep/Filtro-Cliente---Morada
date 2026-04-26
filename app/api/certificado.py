from dataclasses import asdict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.certificado_tradicion import analizar_certificado

router = APIRouter(prefix="/certificado", tags=["certificado"])


class ConsultaPinRequest(BaseModel):
    pin: str


@router.post("/analizar")
def analizar_ctl(req: ConsultaPinRequest):
    pin = req.pin.strip()
    if not pin:
        raise HTTPException(status_code=400, detail="El PIN es obligatorio")

    resultado = analizar_certificado(pin)

    if resultado.error:
        raise HTTPException(status_code=422, detail=resultado.error)

    data = asdict(resultado)
    if data["ultima_compraventa"] is None:
        data["ultima_compraventa"] = None

    return data
