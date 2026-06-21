from src.application.dtos.chatwoot_contact_dto import ChatwootContactDto
from src.domain.entities.lead import Lead


def lead_to_chatwoot_contact(lead: Lead) -> ChatwootContactDto:
    """Traduce una entidad Lead al DTO esperado por Chatwoot Application API."""
    return ChatwootContactDto(
        email=lead.contact.email,
        phone_number=lead.contact.phone,
        name=lead.contact.name,
        additional_attributes={
            "company_name": lead.contact.company,
            "comment": lead.comment,
            "page_location": lead.page_location,
            "traffic_source": lead.traffic_source,
            "preferred_contact_channel": lead.preferred_contact_channel,
        },
    )
