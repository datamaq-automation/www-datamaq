from abc import ABC, abstractmethod
from typing import Any, Dict

from src.domain.entities.lead import Lead


class ChatwootGateway(ABC):
    """Puerto de salida para integración con Chatwoot Application API."""

    @abstractmethod
    async def create_contact_and_conversation(self, lead: Lead) -> Dict[str, Any]:
        """Crea un contacto y una conversación en Chatwoot a partir de un lead."""
        raise NotImplementedError
