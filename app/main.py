from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.filtro import router as filtro_router
from app.api.cliente import router as cliente_router
from app.api.certificado import router as certificado_router
from app.api.documentos import router as documentos_router
from app.api.experian import router as experian_router
from app.api.gastos import router as gastos_router

app = FastAPI(
    title="Morada Capital — Filtro de Originación",
    description="API para evaluación de capacidad de pago de créditos de vivienda",
    version="0.1.0",
)

app.include_router(filtro_router)
app.include_router(gastos_router)
app.include_router(cliente_router)
app.include_router(certificado_router)
app.include_router(documentos_router)
app.include_router(experian_router)

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


@app.middleware("http")
async def sin_cache_estaticos(request, call_next):
    """Obliga al navegador a revalidar HTML y JS en cada carga.

    Sin esto el navegador reutiliza copias viejas de /static (por ejemplo
    solicitantes.js) tras un cambio y las páginas fallan a medio cargar.
    La revalidación usa el ETag, así que el costo es mínimo.
    """
    response = await call_next(request)
    ctype = response.headers.get("content-type", "")
    if request.url.path.startswith("/static") or "text/html" in ctype:
        response.headers["Cache-Control"] = "no-cache"
    return response


@app.get("/")
def root():
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.get("/muestra")
def muestra():
    return FileResponse(str(STATIC_DIR / "muestra.html"))


@app.get("/analista")
def analista():
    return FileResponse(str(STATIC_DIR / "analista.html"))


@app.get("/analisis-ctl")
@app.get("/analisis-arriendos")
def analisis_ctl():
    return FileResponse(str(STATIC_DIR / "analisis_ctl.html"))


@app.get("/gastos-basicos")
def gastos_basicos():
    return FileResponse(str(STATIC_DIR / "gastos_basicos.html"))


@app.get("/carpeta")
def carpeta():
    return FileResponse(str(STATIC_DIR / "carpeta_documentos.html"))


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/health")
def health():
    return {"status": "ok"}
