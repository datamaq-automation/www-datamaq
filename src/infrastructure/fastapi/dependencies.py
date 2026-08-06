from typing import Any, Dict, cast
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from starlette.types import Scope
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger
from src.domain.models import ContenidoModel, LandingContentModel
from src.application.data_service import DataService
from src.application.gateways.notification_gateway import NotificationGateway
from src.infrastructure.gateways.notification_gateway_stub import NotificationGatewayStub
from src.infrastructure.gateways.email_notification_gateway import EmailNotificationGateway
from src.domain.repositories.lead_repository import LeadRepository
from src.infrastructure.persistence.json.lead_repository_json import LeadRepositoryJson
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
data_service = DataService(data_dir="data")

# --- Dependencias de Datos ---
def get_contenido() -> ContenidoModel: return data_service.get_contenido()
def get_geografia(): return data_service.get_geografia()
def get_industrias(): return data_service.get_industrias()
def get_cursos_service() -> DataService: return data_service
def get_redirects() -> Dict[str, str]: return data_service.get_redirects()
def get_landing_content() -> LandingContentModel: return data_service.get_landing_content()

# --- Dependencias de Infraestructura (Repository + Gateway) ---
def get_lead_repository() -> LeadRepository:
    return LeadRepositoryJson()

def get_notification_gateway() -> NotificationGateway:
    if config.SMTP_USERNAME and config.SMTP_PASSWORD and config.NOTIFICATION_EMAIL:
        return EmailNotificationGateway(
            host=config.SMTP_HOST,
            port=config.SMTP_PORT,
            username=config.SMTP_USERNAME,
            password=config.SMTP_PASSWORD,
            to_email=config.NOTIFICATION_EMAIL,
        )
    logger.warning("[dependencies] SMTP_USERNAME, SMTP_PASSWORD o NOTIFICATION_EMAIL no configurados; usando NotificationGatewayStub")
    return NotificationGatewayStub()

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
