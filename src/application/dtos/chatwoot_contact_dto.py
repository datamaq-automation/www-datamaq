from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ChatwootContactDto:
    """DTO para crear un contacto en Chatwoot Application API."""
    email: Optional[str]
    phone_number: Optional[str]
    name: str
    additional_attributes: dict
