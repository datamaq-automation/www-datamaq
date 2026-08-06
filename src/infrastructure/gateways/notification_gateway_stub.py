from typing import Any, Dict

from src.application.gateways.notification_gateway import NotificationGateway
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger

logger = setup_logger(config.LOGGER_NAME)


class NotificationGatewayStub(NotificationGateway):
    """Stub del gateway de notificaciones: no envía emails, solo loguea."""

    async def notify_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(
            "[NotificationGatewayStub] Lead recibido — notificación simulada para: name=%s, email=%s, phone=%s",
            lead_data.get("name"),
            lead_data.get("email") or "sin email",
            lead_data.get("phone") or "sin teléfono",
        )
        logger.debug("[NotificationGatewayStub] Datos completos del lead: %s", lead_data)

        return {
            "status": "stubbed",
            "message": "Notificación simulada (SMTP no configurado)",
        }
