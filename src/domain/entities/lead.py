from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from src.domain.value_objects.contact_info import ContactInfo


@dataclass(frozen=True)
class LeadId:
    """Value Object que representa la identidad de un lead."""
    value: UUID = field(default_factory=uuid4)

    def __str__(self) -> str:
        return f"lead_{self.value.hex[:8]}"


@dataclass
class Lead:
    """Entidad de dominio: una solicitud de contacto recibida."""
    id: LeadId
    contact: ContactInfo
    comment: str
    preferred_contact_channel: str
    page_location: Optional[str]
    traffic_source: Optional[str]
    user_agent: Optional[str]
    geographic_location: Optional[str]
    created_at: str
    captcha_token: Optional[str] = None
