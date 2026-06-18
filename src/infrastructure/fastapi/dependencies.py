from typing import Any, Dict, cast
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from starlette.types import Scope
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger
from src.application.data_service import DataService
import subprocess
import time
import os
from datetime import datetime

logger = setup_logger(config.LOGGER_NAME)

# --- Instancias compartidas ---

class CachedStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope: Scope) -> Response:
        response = await super().get_response(path, scope)
        # En desarrollo desactivamos caché inmutable
        if config.DEBUG:
             response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        else:
             response.headers["Cache-Control"] = f"public, max-age={config.STATIC_CACHE_SECONDS}, immutable"
        return response

templates = Jinja2Templates(directory=config.TEMPLATES_DIR)
templates.env.globals = cast(Dict[str, Any], templates.env.globals)  # type: ignore[assignment]

# --- Configuración del Servicio de Datos ---
data_service = DataService(
    content_path=config.CONTENT_DATA_PATH,
    geography_path=os.path.join(os.path.dirname(config.CONTENT_DATA_PATH), "geografia.yaml"),
    industry_path=os.path.join(os.path.dirname(config.CONTENT_DATA_PATH), "industrias.yaml")
)

# --- Dependencias de Datos ---
def get_contenido(): return data_service.get_contenido()
def get_geografia(): return data_service.get_geografia()
def get_industrias(): return data_service.get_industrias()
def get_chatwoot_token() -> str:
    return config.CHATWOOT_TOKEN or ""

# --- Configuración Jinja2 ---
def get_static_version() -> str:
    if config.DEBUG:
        return str(int(time.time()))
    
    try:
        return subprocess.check_output(["/usr/bin/git", "rev-parse", "--short", "HEAD"]).decode("ascii").strip()
    except Exception as e:
        logger.warning(f"No se pudo obtener el hash de git. Error: {e}. Usando timestamp.")
        return str(int(time.time()))

templates.env.globals["static_version"] = get_static_version  # type: ignore[index]
templates.env.globals["config"] = config  # type: ignore[index]
templates.env.globals["year"] = datetime.now().year
