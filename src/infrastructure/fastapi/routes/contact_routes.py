from typing import Any, Dict
from fastapi import APIRouter, HTTPException, Request, Depends
from src.domain.models import ContactSubmitPayload, ContenidoModel
from src.domain.repositories.lead_repository import LeadRepository
from src.application.gateways.chatwoot_gateway import ChatwootGateway
from src.infrastructure.fastapi.dependencies import (
    templates,
    get_contenido,
    get_chatwoot_token,
    get_lead_repository,
    get_chatwoot_gateway,
)
from src.infrastructure.fastapi.utils.seo import canonical_url
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger
from src.application.use_cases.submit_lead import SubmitLeadUseCase

router = APIRouter()
logger = setup_logger(config.LOGGER_NAME)


@router.get("/contact")
async def contact_page(request: Request, contenido: ContenidoModel = Depends(get_contenido), chatwoot_token: str = Depends(get_chatwoot_token)):
    base_seo = contenido.seo.model_dump()
    seo = {
        **base_seo,
        "title": f"Consultoría técnica IoT | {contenido.brand.brandName}",
        "description": f"Contactá a {contenido.brand.brandName} para una consultoría técnica sobre monitoreo de energía industrial, captura de datos operativos e IoT industrial.",
        "canonical_url": canonical_url(request.url),
        "og_image_width": 1200,
        "og_image_height": 630,
    }
    context: Dict[str, Any] = {
        "brand": contenido.brand.model_dump(),
        "content": contenido.content.model_dump(),
        "seo": seo,
        "chatwoot_token": chatwoot_token,
        "contact_hero": {
            "title": f"Consultoría técnica IoT con {contenido.brand.brandName}",
            "subtitle": "Escribinos para evaluar tu proyecto de monitoreo de energía industrial, captura de datos operativos o equipos IoT.",
        },
    }
    return templates.TemplateResponse(request=request, name="contact.html", context=context)


@router.post("/api/v1/contact", status_code=201)
async def submit_contact(
    payload: ContactSubmitPayload,
    repository: LeadRepository = Depends(get_lead_repository),
    chatwoot_gateway: ChatwootGateway = Depends(get_chatwoot_gateway),
):
    logger.info("[submit_contact] Recibiendo POST /api/v1/contact")
    logger.debug("[submit_contact] Payload validado: name presente=%s, email presente=%s, phone presente=%s",
                 bool(payload.name), bool(payload.email), bool(payload.phone))

    try:
        use_case = SubmitLeadUseCase(repository=repository, chatwoot_gateway=chatwoot_gateway)
        result = await use_case.execute(payload)
        logger.info("[submit_contact] Lead procesado: submission_id=%s, status=%s", result.submission_id, result.submit_status)
        return use_case.to_http_response(result)
    except Exception as e:
        logger.error("[submit_contact] Error inesperado al procesar lead: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
