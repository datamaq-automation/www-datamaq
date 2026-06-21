from typing import Any, Dict
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, Depends
from src.domain.models import ContactSubmitPayload, ContenidoModel
from src.infrastructure.fastapi.dependencies import templates, get_contenido, get_chatwoot_token
from src.infrastructure.fastapi.utils.seo import canonical_url
from src.application.use_cases.submit_lead import SubmitLeadUseCase
from src.infrastructure.persistence.json.lead_repository_json import LeadRepositoryJson

router = APIRouter()
submit_lead_use_case = SubmitLeadUseCase(repository=LeadRepositoryJson())

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
async def submit_contact(payload: ContactSubmitPayload, background_tasks: BackgroundTasks):
    try:
        return submit_lead_use_case.execute(payload, background_tasks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
