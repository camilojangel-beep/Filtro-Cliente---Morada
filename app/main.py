from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.filtro import router as filtro_router

app = FastAPI(
    title="Morada Capital — Filtro de Originación",
    description="API para evaluación de capacidad de pago de créditos de vivienda",
    version="0.1.0",
)

app.include_router(filtro_router)

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def root():
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.get("/health")
def health():
    return {"status": "ok"}
