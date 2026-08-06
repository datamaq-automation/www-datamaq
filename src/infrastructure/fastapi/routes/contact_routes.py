from typing import Any, Dict
from fastapi import APIRouter, HTTPException, Request, Depends
from src.domain.models import ContactSubmitPayload, ContenidoModel
from src.domain.repositories.lead_repository import LeadRepository
from src.application.gateways.notification_gateway import NotificationGateway
from src.infrastructure.fastapi.dependencies import (
    templates,
    get_contenido,
    get_lead_repository,
    get_notification_gateway,
)
from src.infrastructure.fastapi.utils.seo import canonical_url
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger
from src.application.use_cases.submit_lead import SubmitLeadUseCase
from src.adapters.presenters.content_presenter import present_contenido

router = APIRouter()
logger = setup_logger(config.LOGGER_NAME)

@router.get("/contact")
async def contact_page(request: Request, contenido: ContenidoModel = Depends(get_contenido)):
    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]
    contact_data = content_data["contact"]

    base_seo = presented["seo"]
    seo = {
        **base_seo,
        "title": f"{contact_data['title']} | {brand_data['brandName']}",
        "description": contact_data["subtitle"],
        "canonical_url": canonical_url(request.url),
        "og_image_width": 1200,
        "og_image_height": 630,
    }
    context: Dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "seo": seo,
        "footer": presented.get("footer"),
        "contact_hero": {
            "title": f"{contact_data['title']} con {brand_data['brandName']}",
            "subtitle": contact_data["subtitle"],
        },
    }
    return templates.TemplateResponse(request=request, name="contact.html", context=context)

@router.post("/api/v1/contact", status_code=201)
async def submit_contact(
    payload: ContactSubmitPayload,
    repository: LeadRepository = Depends(get_lead_repository),
    notification_gateway: NotificationGateway = Depends(get_notification_gateway),
):
    logger.info("[submit_contact] Recibiendo POST /api/v1/contact")
    logger.debug("[submit_contact] Payload validado: name presente=%s, email presente=%s, phone presente=%s",
                 bool(payload.name), bool(payload.email), bool(payload.phone))

    try:
        use_case = SubmitLeadUseCase(repository=repository, notification_gateway=notification_gateway)
        result = await use_case.execute(payload)
        logger.info("[submit_contact] Lead procesado: submission_id=%s, status=%s", result.submission_id, result.submit_status)
        return {
            "requestId": result.request_id,
            "submissionId": result.submission_id,
            "submitStatus": result.submit_status,
        }
    except Exception as e:
        logger.error("[submit_contact] Error inesperado al procesar lead: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
