from abc import ABC, abstractmethod
from typing import Any, Dict


class NotificationGateway(ABC):
    """Puerto de salida para notificaciones de nuevos leads."""

    @abstractmethod
    async def notify_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Notifica un nuevo lead al técnico (email, push, etc.)."""
        raise NotImplementedError
