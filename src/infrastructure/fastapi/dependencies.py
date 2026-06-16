from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from starlette.types import Scope
from src.infrastructure.settings import config
from src.infrastructure.fastapi.schemas import ContenidoModel, IndustriaModel
from typing import Any, Dict, cast
import subprocess
import time
import logging
import yaml
import os

logger = logging.getLogger(config.LOGGER_NAME)

# --- Instancias compartidas ---

class CachedStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope: Scope) -> Response:
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = f"public, max-age={config.STATIC_CACHE_SECONDS}, immutable"
        return response

templates = Jinja2Templates(directory=config.TEMPLATES_DIR)

# --- Dependencias de Datos ---
def get_contenido() -> ContenidoModel:
    with open(config.CONTENT_DATA_PATH, "r", encoding="utf-8") as f:
        raw_data: Dict[str, Any] = yaml.safe_load(f) # type: ignore
        return ContenidoModel(**raw_data)

def get_geografia() -> Dict[str, Any]:
    geografia_path = os.path.join(os.path.dirname(config.CONTENT_DATA_PATH), "geografia.yaml")
    with open(geografia_path, "r", encoding="utf-8") as f:
        return cast(Dict[str, Any], yaml.safe_load(f)) # type: ignore

def get_industrias() -> IndustriaModel:
    industrias_path = os.path.join(os.path.dirname(config.CONTENT_DATA_PATH), "industrias.yaml")
    with open(industrias_path, "r", encoding="utf-8") as f:
        raw_data: Dict[str, Any] = yaml.safe_load(f) # type: ignore
        return IndustriaModel(**raw_data)

def get_chatwoot_token() -> str:
    # Aseguramos que retorne str, incluso si es None en la config, retornamos string vacío
    return config.CHATWOOT_TOKEN or ""

# --- Configuración Jinja2 ---
def get_static_version_hash() -> str:
    try:
        return subprocess.check_output(["/usr/bin/git", "rev-parse", "--short", "HEAD"]).decode("ascii").strip()
    except Exception as e:
        logger.warning(f"No se pudo obtener el hash de git. Error: {e}. Usando timestamp.")
        return str(int(time.time()))

templates.env.globals["static_version"] = get_static_version_hash # type: ignore
templates.env.globals["config"] = config # type: ignore
