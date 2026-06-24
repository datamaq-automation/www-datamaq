from dataclasses import dataclass, field
from typing import Optional, Dict, Any


def _dict_factory() -> Dict[str, Any]:
    return {}


@dataclass(frozen=True)
class ChatwootContactDto:
    """DTO para crear un contacto en Chatwoot Application API."""
    email: Optional[str]
    phone_number: Optional[str]
    name: str
    additional_attributes: Dict[str, Any] = field(default_factory=_dict_factory)
    custom_attributes: Dict[str, Any] = field(default_factory=_dict_factory)