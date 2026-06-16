from typing import Any, Dict
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response, FileResponse
from starlette.types import Scope
from src.infrastructure.settings.logger import setup_logger
from src.infrastructure.settings import config
from src.infrastructure.fastapi.schemas import ContenidoModel
import yaml
import subprocess
import time
import os

class CachedStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope: Scope) -> Response:
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = f"public, max-age={config.STATIC_CACHE_SECONDS}, immutable"
        return response

app = FastAPI(title=config.APP_TITLE)
app.mount("/static", CachedStaticFiles(directory=config.STATIC_DIR), name="static")

templates = Jinja2Templates(directory=config.TEMPLATES_DIR)

def get_static_version_hash() -> str:
    try:
        return subprocess.check_output(["/usr/bin/git", "rev-parse", "--short", "HEAD"]).decode("ascii").strip()
    except Exception as e:
        logger.warning(f"No se pudo obtener el hash de git. Error: {e}. Usando timestamp.")
        return str(int(time.time()))

templates.env.globals["static_version"] = get_static_version_hash # type: ignore
templates.env.globals["config"] = config # type: ignore

logger = setup_logger(config.LOGGER_NAME)

def cargar_datos() -> tuple[ContenidoModel, Dict[str, Any]]:
    with open(config.CONTENT_DATA_PATH, "r", encoding="utf-8") as f:
        # Pylance no puede tipar PyYAML, ignoramos la advertencia en esta línea
        raw_data: Dict[str, Any] = yaml.safe_load(f) # type: ignore
        contenido = ContenidoModel(**raw_data)
    
    geografia_path = os.path.join(os.path.dirname(config.CONTENT_DATA_PATH), "geografia.yaml")
    with open(geografia_path, "r", encoding="utf-8") as f:
        geografia: Dict[str, Any] = yaml.safe_load(f) # type: ignore
        
    return contenido, geografia

contenido, geografia = cargar_datos()
chatwoot_token = config.CHATWOOT_TOKEN

@app.get("/{provincia}/{municipio}/{localidad}.html")
async def pagina_localidad(request: Request, provincia: str, municipio: str, localidad: str):
    # Validar existencia
    locs = geografia.get("localidades", {})
    # Acceso seguro a la estructura de geografía
    prov = locs.get(provincia, {})
    mun = prov.get(municipio, {})
    nombre_localidad = mun.get(localidad)
    
    if not nombre_localidad:
        raise HTTPException(status_code=404, detail="Localidad no encontrada")
        
    context: Dict[str, Any] = {
        "negocio": contenido.negocio.model_dump(),
        "servicios": [s.model_dump() for s in contenido.servicios],
        "faq": contenido.faq,
        "chatwoot_token": chatwoot_token,
        "localidad_nombre": nombre_localidad,
        "municipio": municipio.replace("-", " ").title(),
        "provincia": provincia.replace("-", " ").title(),
        "seo_titulo": f"Electricista en {nombre_localidad}, {municipio.replace("-", " ").title()} - Urgencias 24/7",
        "seo_descripcion": f"¿Necesitas un electricista en {nombre_localidad}? Servicio profesional certificado en {municipio.replace("-", " ").title()}. Atención rápida, segura y 24/7."
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)

@app.get("/robots.txt")
async def robots():
    return FileResponse(config.ROBOTS_TXT_PATH)

@app.get("/sitemap.xml")
async def sitemap(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="sitemap.xml", 
        media_type="application/xml"
    )

@app.get("/dev/preview/{partial_name}")
async def preview(request: Request, partial_name: str):
    context: Dict[str, Any] = {
        "negocio": contenido.negocio.model_dump(),
        "servicios": [s.model_dump() for s in contenido.servicios],
        "faq": contenido.faq,
        "chatwoot_token": chatwoot_token,
        "partial_name": partial_name
    }
    return templates.TemplateResponse(request=request, name="preview.html", context=context)

@app.get("/")
async def root(request: Request):
    logger.info("Acceso a la Landing Page")
    context: Dict[str, Any] = {
        "negocio": contenido.negocio.model_dump(),
        "servicios": [s.model_dump() for s in contenido.servicios],
        "faq": contenido.faq,
        "chatwoot_token": chatwoot_token
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)
