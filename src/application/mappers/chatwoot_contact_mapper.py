from src.application.dtos.chatwoot_contact_dto import ChatwootContactDto
from src.domain.entities.lead import Lead
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger

logger = setup_logger(config.LOGGER_NAME)


def lead_to_chatwoot_contact(lead: Lead) -> ChatwootContactDto:
    """Traduce una entidad Lead al DTO esperado por Chatwoot Application API."""
    logger.debug("[chatwoot_contact_mapper] Mapeando Lead %s a ChatwootContactDto", str(lead.id))

    contact = ChatwootContactDto(
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

    logger.debug("[chatwoot_contact_mapper] DTO generado: name=%s, email=%s, phone=%s",
                 contact.name, bool(contact.email), bool(contact.phone_number))
    return contact
