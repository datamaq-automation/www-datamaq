from typing import Dict
from src.application.gateways.chatwoot_gateway import ChatwootGateway
from src.domain.models import ContactSubmitPayload
from src.domain.entities.lead import Lead, LeadId
from src.domain.repositories.lead_repository import LeadRepository
from src.domain.value_objects.contact_info import ContactInfo
from src.domain.value_objects.lead_submission_result import LeadSubmissionResult
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger
import uuid

logger = setup_logger(config.LOGGER_NAME)


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

    async def execute(self, payload: ContactSubmitPayload) -> LeadSubmissionResult:
        lead = _map_payload_to_lead(payload)
        submission_id = str(lead.id)
        request_id = f"req_{uuid.uuid4().hex[:8]}"

        try:
            await self._repository.save(lead)
        except Exception as e:
            logger.error("[SubmitLeadUseCase] Fallo al guardar lead %s: %s", submission_id, e)
            return LeadSubmissionResult(
                request_id=request_id,
                submission_id=submission_id,
                lead_saved=False,
                chatwoot_synced=False,
                error_message="No se pudo guardar el lead",
            )

        try:
            await self._chatwoot_gateway.create_contact(lead)
        except Exception as e:
            logger.error("[SubmitLeadUseCase] Fallo al sincronizar lead %s con Chatwoot: %s", submission_id, e)
            return LeadSubmissionResult(
                request_id=request_id,
                submission_id=submission_id,
                lead_saved=True,
                chatwoot_synced=False,
                error_message="Lead guardado, pero no se pudo sincronizar con Chatwoot",
            )

        return LeadSubmissionResult(
            request_id=request_id,
            submission_id=submission_id,
            lead_saved=True,
            chatwoot_synced=True,
        )

    def to_http_response(self, result: LeadSubmissionResult) -> Dict[str, str]:
        """Mapea el resultado de dominio al contrato HTTP actual."""
        return {
            "requestId": result.request_id,
            "submissionId": result.submission_id,
            "submitStatus": result.submit_status,
        }
