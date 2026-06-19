from typing import Any, Dict
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, Depends
from src.domain.models import ContactSubmitPayload, ContenidoModel
from src.infrastructure.fastapi.dependencies import templates, get_contenido, get_chatwoot_token
import json
import uuid
import os

router = APIRouter()

@router.get("/contact")
async def contact_page(request: Request, contenido: ContenidoModel = Depends(get_contenido), chatwoot_token: str = Depends(get_chatwoot_token)):
    base_seo = contenido.seo.model_dump()
    seo = {
        **base_seo,
        "title": f"Contacto | {contenido.brand.brandName}",
        "description": f"Contact\u00e1 a {contenido.brand.brandName} para una consulta t\u00e9cnica sobre captura de datos operativos, energ\u00eda y producci\u00f3n.",
        "canonical_url": str(request.url),
    }
    context: Dict[str, Any] = {
        "brand": contenido.brand.model_dump(),
        "content": contenido.content.model_dump(),
        "seo": seo,
        "chatwoot_token": chatwoot_token,
    }
    return templates.TemplateResponse(request=request, name="contact.html", context=context)

# TODO: Migrar a PostgreSQL
DATA_DIR = "data/leads"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

async def persist_lead_task(payload: ContactSubmitPayload, submission_id: str):
    # Simulación de persistencia en DB y reenvío asíncrono
    lead_path = os.path.join(DATA_DIR, f"{submission_id}.json")
    with open(lead_path, "w", encoding="utf-8") as f:
        json.dump(payload.model_dump(), f, indent=2, ensure_ascii=False)
    # Aquí iría la lógica de reenvío a CRM/Google Sheets

@router.post("/api/v1/contact", status_code=201)
async def submit_contact(payload: ContactSubmitPayload, background_tasks: BackgroundTasks):
    try:
        submission_id = f"lead_{uuid.uuid4().hex[:8]}"
        request_id = f"req_{uuid.uuid4().hex[:8]}"
        
        background_tasks.add_task(persist_lead_task, payload, submission_id)
        
        return {
            "requestId": request_id,
            "submissionId": submission_id,
            "submitStatus": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
