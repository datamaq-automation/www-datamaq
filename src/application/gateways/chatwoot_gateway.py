from abc import ABC, abstractmethod
from typing import Any, Dict

from src.application.dtos.chatwoot_contact_dto import ChatwootContactDto


class ChatwootGateway(ABC):
    """Puerto de salida para integración con Chatwoot Application API."""

    @abstractmethod
    async def create_contact(self, contact: ChatwootContactDto) -> Dict[str, Any]:
        """Crea un contacto en Chatwoot a partir de un DTO de contacto."""
        raise NotImplementedError
