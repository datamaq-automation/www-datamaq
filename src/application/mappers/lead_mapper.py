from src.domain.models import ContactSubmitPayload
from src.domain.entities.lead import Lead, LeadId
from src.domain.value_objects.contact_info import ContactInfo
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger

logger = setup_logger(config.LOGGER_NAME)


def payload_to_lead(payload: ContactSubmitPayload) -> Lead:
    """Traduce el payload de entrada del formulario en una entidad de dominio Lead."""
    logger.debug("[lead_mapper] Mapeando ContactSubmitPayload a Lead")

    lead = Lead(
        id=LeadId(),
        contact=ContactInfo(
            name=payload.name,
            first_name=payload.firstName,
            last_name=payload.lastName,
            email=payload.email,
            phone=payload.phone,
            company=payload.company,
        ),
        comment=payload.comment,
        preferred_contact_channel=payload.preferredContactChannel,
        page_location=payload.pageLocation,
        traffic_source=payload.trafficSource,
        user_agent=payload.userAgent,
        geographic_location=payload.geographicLocation,
        created_at=payload.createdAt,
        captcha_token=payload.captchaToken,
    )

    logger.debug("[lead_mapper] Lead generado: id=%s, canales=%s, page=%s",
                 str(lead.id), lead.preferred_contact_channel, lead.page_location)
    return lead
