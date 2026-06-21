from typing import Any, Dict
from fastapi import BackgroundTasks
from src.application.gateways.chatwoot_gateway import ChatwootGateway
from src.domain.models import ContactSubmitPayload
from src.domain.entities.lead import Lead, LeadId
from src.domain.repositories.lead_repository import LeadRepository
from src.domain.value_objects.contact_info import ContactInfo
import uuid


def _map_payload_to_lead(payload: ContactSubmitPayload) -> Lead:
    """Traduce el payload de entrada en una entidad de dominio Lead."""
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


class SubmitLeadUseCase:
    """Caso de uso que orquesta la recepción, persistencia y sincronización de un lead."""

    def __init__(self, repository: LeadRepository, chatwoot_gateway: ChatwootGateway):
        self._repository = repository
        self._chatwoot_gateway = chatwoot_gateway

    def execute(self, payload: ContactSubmitPayload, background_tasks: BackgroundTasks) -> Dict[str, Any]:
        lead = _map_payload_to_lead(payload)
        submission_id = str(lead.id)
        request_id = f"req_{uuid.uuid4().hex[:8]}"

        background_tasks.add_task(self._repository.save, lead)
        background_tasks.add_task(self._chatwoot_gateway.create_contact, lead)

        return {
            "requestId": request_id,
            "submissionId": submission_id,
            "submitStatus": "success"
        }
