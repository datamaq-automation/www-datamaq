from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ContactInfo:
    """Value Object con los datos de contacto de un lead."""
    name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
