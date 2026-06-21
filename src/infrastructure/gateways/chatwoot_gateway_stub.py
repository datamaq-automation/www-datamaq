from typing import Any, Dict

from src.application.gateways.chatwoot_gateway import ChatwootGateway
from src.domain.entities.lead import Lead
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger

logger = setup_logger(config.LOGGER_NAME)


class ChatwootGatewayStub(ChatwootGateway):
    """Stub del gateway de Chatwoot: no realiza llamadas HTTP."""

    async def create_contact_and_conversation(self, lead: Lead) -> Dict[str, Any]:
        logger.info(
            "[ChatwootGatewayStub] Simulando creación de contacto/conversación para lead %s (%s)",
            str(lead.id),
            lead.contact.email or lead.contact.phone or "sin contacto directo",
        )
        return {
            "contact_id": "stub_contact_id",
            "conversation_id": "stub_conversation_id",
            "status": "stubbed",
        }
