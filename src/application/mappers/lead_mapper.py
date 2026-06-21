from src.domain.models import ContactSubmitPayload
from src.domain.entities.lead import Lead, LeadId
from src.domain.value_objects.contact_info import ContactInfo


def payload_to_lead(payload: ContactSubmitPayload) -> Lead:
    """Traduce el payload de entrada del formulario en una entidad de dominio Lead."""
    return Lead(
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
