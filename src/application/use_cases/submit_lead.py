from typing import Dict
from src.application.dtos.chatwoot_contact_dto import ChatwootContactDto
from src.application.gateways.chatwoot_gateway import ChatwootGateway
from src.application.mappers.chatwoot_contact_mapper import lead_to_chatwoot_contact
from src.application.mappers.lead_mapper import payload_to_lead
from src.domain.models import ContactSubmitPayload
from src.domain.repositories.lead_repository import LeadRepository
from src.domain.value_objects.lead_submission_result import LeadSubmissionResult
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger
import uuid

logger = setup_logger(config.LOGGER_NAME)


class SubmitLeadUseCase:
    """Caso de uso que orquesta la recepción, persistencia y sincronización de un lead."""

    def __init__(self, repository: LeadRepository, chatwoot_gateway: ChatwootGateway):
        self._repository = repository
        self._chatwoot_gateway = chatwoot_gateway

    async def execute(self, payload: ContactSubmitPayload) -> LeadSubmissionResult:
        lead = payload_to_lead(payload)
        chatwoot_contact = lead_to_chatwoot_contact(lead)
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
            await self._chatwoot_gateway.create_contact(chatwoot_contact)
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
