from fastapi import APIRouter

from app.models.solicitud import EvaluarIngresoRequest, EvaluarIngresoResponse
from app.services.ingreso import evaluar_ingreso

router = APIRouter(prefix="/filtro", tags=["Filtro de Originación"])


@router.post("/evaluar-ingreso", response_model=EvaluarIngresoResponse)
def endpoint_evaluar_ingreso(request: EvaluarIngresoRequest):
    return evaluar_ingreso(request)
