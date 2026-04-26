from fastapi import APIRouter, HTTPException

from app.models.cliente import DatosBasicosCliente

router = APIRouter(prefix="/cliente", tags=["Cliente"])


@router.post("/registrar")
def registrar_cliente(datos: DatosBasicosCliente):
    if not datos.autorizacion_aceptada:
        raise HTTPException(
            status_code=400,
            detail="Debe aceptar la autorización de consulta y tratamiento de datos",
        )

    respuesta = {
        "status": "ok",
        "mensaje": "Datos registrados exitosamente",
        "cliente": {
            "nombre": f"{datos.primer_nombre} {datos.primer_apellido}",
            "tipo_identificacion": datos.tipo_identificacion.value,
            "numero_identificacion": datos.numero_identificacion,
        },
    }

    if datos.segundo_solicitante:
        s = datos.segundo_solicitante
        respuesta["segundo_solicitante"] = {
            "nombre": f"{s.primer_nombre} {s.primer_apellido}",
            "tipo_identificacion": s.tipo_identificacion.value,
            "numero_identificacion": s.numero_identificacion,
        }
        respuesta["parentesco"] = datos.parentesco

    return respuesta
