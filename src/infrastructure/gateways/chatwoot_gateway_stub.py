from typing import Any, Dict

from src.application.dtos.chatwoot_contact_dto import ChatwootContactDto
from src.application.gateways.chatwoot_gateway import ChatwootGateway
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger

logger = setup_logger(config.LOGGER_NAME)


class ChatwootGatewayStub(ChatwootGateway):
    """Stub del gateway de Chatwoot: no realiza llamadas HTTP."""

    async def create_contact(self, contact: ChatwootContactDto) -> Dict[str, Any]:
        logger.debug("[ChatwootGatewayStub] Preparando contacto para Chatwoot: name=%s", contact.name)

        logger.info(
            "[ChatwootGatewayStub] Simulando creación de contacto para %s (%s)",
            contact.name,
            contact.email or contact.phone_number or "sin contacto directo",
        )

        if not contact.email and not contact.phone_number:
            logger.warning("[ChatwootGatewayStub] Contacto sin email ni teléfono: name=%s", contact.name)

        return {
            "contact_id": "stub_contact_id",
            "status": "stubbed",
        }
