import os
import uuid
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.services.contrato_arrendamiento import analizar_contrato

router = APIRouter(prefix="/documentos", tags=["documentos"])

UPLOADS_DIR = Path(__file__).resolve().parent.parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)


def _carpeta_solicitante(numero_id: str) -> Path:
    carpeta = UPLOADS_DIR / numero_id
    carpeta.mkdir(exist_ok=True)
    return carpeta


@router.post("/subir-contrato")
async def subir_contrato(
    numero_identificacion: str = Form(...),
    pin_certificado: str = Form(""),
    indice_inmueble: int = Form(0),
    archivo: UploadFile = File(...),
):
    if not archivo.filename:
        raise HTTPException(status_code=400, detail="Archivo vacío")

    ext = Path(archivo.filename).suffix
    carpeta = _carpeta_solicitante(numero_identificacion)
    carpeta_arriendos = carpeta / "arriendos"
    carpeta_arriendos.mkdir(exist_ok=True)

    nombre = f"contrato_inmueble_{indice_inmueble}{ext}"
    ruta = carpeta_arriendos / nombre

    contenido = await archivo.read()
    ruta.write_bytes(contenido)

    meta_path = carpeta_arriendos / f"contrato_inmueble_{indice_inmueble}.meta"
    meta_path.write_text(f"pin={pin_certificado}\narchivo={nombre}\n")

    return {
        "status": "ok",
        "archivo": nombre,
        "ruta": str(ruta.relative_to(UPLOADS_DIR)),
    }


@router.post("/subir-central")
async def subir_central(
    numero_identificacion: str = Form(...),
    archivo: UploadFile = File(...),
):
    if not archivo.filename:
        raise HTTPException(status_code=400, detail="Archivo vacío")

    ext = Path(archivo.filename).suffix
    carpeta = _carpeta_solicitante(numero_identificacion)
    carpeta_centrales = carpeta / "centrales"
    carpeta_centrales.mkdir(exist_ok=True)

    nombre = f"consulta_central{ext}"
    ruta = carpeta_centrales / nombre

    contenido = await archivo.read()
    ruta.write_bytes(contenido)

    return {
        "status": "ok",
        "archivo": nombre,
        "ruta": str(ruta.relative_to(UPLOADS_DIR)),
    }


@router.get("/listar/{numero_identificacion}")
def listar_documentos(numero_identificacion: str):
    carpeta = UPLOADS_DIR / numero_identificacion
    if not carpeta.exists():
        return {"centrales": [], "arriendos": []}

    centrales = []
    carpeta_centrales = carpeta / "centrales"
    if carpeta_centrales.exists():
        for f in carpeta_centrales.iterdir():
            if not f.name.endswith(".meta"):
                centrales.append({"nombre": f.name, "ruta": f"/documentos/archivo/{numero_identificacion}/centrales/{f.name}"})

    arriendos = []
    carpeta_arriendos = carpeta / "arriendos"
    if carpeta_arriendos.exists():
        contratos = {}
        metas = {}
        for f in carpeta_arriendos.iterdir():
            if f.name.endswith(".meta"):
                metas[f.stem] = dict(
                    line.split("=", 1) for line in f.read_text().strip().split("\n") if "=" in line
                )
            else:
                base = f.stem.rsplit(".", 1)[0] if "." in f.stem else f.stem
                contratos[base] = {
                    "nombre": f.name,
                    "ruta": f"/documentos/archivo/{numero_identificacion}/arriendos/{f.name}",
                }
        for key, contrato in contratos.items():
            meta = metas.get(key, {})
            arriendos.append({
                "pin": meta.get("pin", ""),
                "contrato": contrato,
            })

    return {"centrales": centrales, "arriendos": arriendos}


class AnalisisContratoRequest(BaseModel):
    numero_identificacion: str
    indice_inmueble: int


@router.post("/analizar-contrato")
def endpoint_analizar_contrato(req: AnalisisContratoRequest):
    carpeta = UPLOADS_DIR / req.numero_identificacion / "arriendos"
    if not carpeta.exists():
        raise HTTPException(status_code=404, detail="No se encontraron documentos para este solicitante")

    archivo = None
    for ext in [".pdf", ".png", ".jpg", ".jpeg", ".docx", ".doc"]:
        candidato = carpeta / f"contrato_inmueble_{req.indice_inmueble}{ext}"
        if candidato.exists():
            archivo = candidato
            break

    if not archivo:
        raise HTTPException(status_code=404, detail="No se encontró contrato para este inmueble")

    resultado = analizar_contrato(str(archivo))
    if resultado.error:
        raise HTTPException(status_code=422, detail=resultado.error)

    return {
        "fecha_firma": resultado.fecha_firma,
        "direccion": resultado.direccion,
        "nomenclatura": resultado.nomenclatura,
        "arrendadores": resultado.arrendadores,
        "canon_mensual": resultado.canon_mensual,
        "texto_completo": resultado.texto_completo,
    }


@router.get("/archivo/{numero_identificacion}/{subcarpeta}/{nombre_archivo}")
def descargar_archivo(numero_identificacion: str, subcarpeta: str, nombre_archivo: str):
    if subcarpeta not in ("centrales", "arriendos"):
        raise HTTPException(status_code=400, detail="Subcarpeta inválida")

    ruta = UPLOADS_DIR / numero_identificacion / subcarpeta / nombre_archivo
    if not ruta.exists():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    return FileResponse(str(ruta), filename=nombre_archivo)
