
from src.application.gateways.notification_gateway import NotificationGateway
from src.application.mappers.lead_mapper import payload_to_lead
from src.domain.models import ContactSubmitPayload
from src.domain.repositories.lead_repository import LeadRepository
from src.domain.value_objects.lead_submission_result import LeadSubmissionResult
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger
import uuid

logger = setup_logger(config.LOGGER_NAME)


class SubmitLeadUseCase:
    """Caso de uso que orquesta la recepción, persistencia y notificación de un lead."""

    def __init__(self, repository: LeadRepository, notification_gateway: NotificationGateway):
        self._repository = repository
        self._notification_gateway = notification_gateway

    async def execute(self, payload: ContactSubmitPayload) -> LeadSubmissionResult:
        logger.info("[SubmitLeadUseCase] Iniciando procesamiento de lead")
        logger.debug("[SubmitLeadUseCase] Campos del payload: name=%s, email=%s, phone=%s, company=%s",
                     payload.name, bool(payload.email), bool(payload.phone), bool(payload.company))

        lead = payload_to_lead(payload)
        submission_id = str(lead.id)
        request_id = f"req_{uuid.uuid4().hex[:8]}"

        logger.info("[SubmitLeadUseCase] Lead mapeado: submission_id=%s", submission_id)

        try:
            await self._repository.save(lead)
            logger.info("[SubmitLeadUseCase] Lead %s persistido correctamente", submission_id)
        except Exception as e:
            logger.error("[SubmitLeadUseCase] Fallo al persistir lead %s: %s", submission_id, e)
            return LeadSubmissionResult(
                request_id=request_id,
                submission_id=submission_id,
                lead_saved=False,
                notification_sent=False,
                error_message="No se pudo guardar el lead",
            )

        lead_data = {
            "name": lead.contact.name,
            "email": lead.contact.email,
            "phone": lead.contact.phone,
            "company": lead.contact.company,
            "comment": lead.comment,
            "source": lead.preferred_contact_channel,
        }

        try:
            await self._notification_gateway.notify_lead(lead_data)
            logger.info("[SubmitLeadUseCase] Lead %s notificado correctamente", submission_id)
        except Exception as e:
            logger.warning("[SubmitLeadUseCase] Fallo al notificar lead %s: %s", submission_id, e)
            return LeadSubmissionResult(
                request_id=request_id,
                submission_id=submission_id,
                lead_saved=True,
                notification_sent=False,
                error_message="Lead guardado, pero no se pudo enviar la notificación",
            )

        logger.info("[SubmitLeadUseCase] Procesamiento de lead %s completado exitosamente", submission_id)
        return LeadSubmissionResult(
            request_id=request_id,
            submission_id=submission_id,
            lead_saved=True,
            notification_sent=True,
        )
