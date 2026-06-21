from typing import Any, Dict

import httpx

from src.application.dtos.chatwoot_contact_dto import ChatwootContactDto
from src.application.gateways.chatwoot_gateway import ChatwootGateway
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger

logger = setup_logger(config.LOGGER_NAME)


class ChatwootGatewayHttp(ChatwootGateway):
    """Implementación HTTP real del gateway de Chatwoot usando httpx."""

    def __init__(self, base_url: str, account_id: str, api_token: str, timeout: float = 10.0):
        self._base_url = base_url.rstrip("/")
        self._account_id = account_id
        self._api_token = api_token
        self._timeout = timeout

    async def create_contact(self, contact: ChatwootContactDto) -> Dict[str, Any]:
        url = f"{self._base_url}/api/v1/accounts/{self._account_id}/contacts"
        headers = {
            "api_access_token": self._api_token,
            "Content-Type": "application/json",
        }
        payload = {
            "email": contact.email,
            "phone_number": contact.phone_number,
            "name": contact.name,
            "additional_attributes": contact.additional_attributes,
        }

        logger.info("[ChatwootGatewayHttp] Creando contacto en Chatwoot: name=%s", contact.name)
        logger.debug("[ChatwootGatewayHttp] POST %s", url)

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            try:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                logger.error(
                    "[ChatwootGatewayHttp] Error HTTP %s al crear contacto: %s",
                    e.response.status_code,
                    e.response.text,
                )
                raise

        data = response.json()
        contact_id = data.get("payload", {}).get("contact", {}).get("id")
        logger.info("[ChatwootGatewayHttp] Contacto creado: id=%s", contact_id)
        return data
