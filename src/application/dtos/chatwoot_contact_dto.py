from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class ChatwootContactDto:
    """DTO para crear un contacto en Chatwoot Application API."""
    email: Optional[str]
    phone_number: Optional[str]
    name: str
    additional_attributes: dict = field(default_factory=dict)
    custom_attributes: dict = field(default_factory=dict)