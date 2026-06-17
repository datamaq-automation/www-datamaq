from typing import Any, Dict
from fastapi import APIRouter, Request, Depends
from fastapi.responses import FileResponse
from src.infrastructure.settings import config
from src.infrastructure.fastapi.dependencies import templates, get_contenido, get_chatwoot_token
from src.domain.models import ContenidoModel

router = APIRouter()

@router.get("/robots.txt")
async def robots():
    return FileResponse(config.ROBOTS_TXT_PATH)

@router.get("/sitemap.xml")
async def sitemap(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="sitemap.xml", 
        media_type="application/xml"
    )

@router.get("/dev/preview/{partial_name}")
async def preview(request: Request, partial_name: str, contenido: ContenidoModel = Depends(get_contenido), chatwoot_token: str = Depends(get_chatwoot_token)):
    context: Dict[str, Any] = {
        "brand": contenido.brand.model_dump(),
        "content": contenido.content.model_dump(),
        "seo": contenido.seo.model_dump(),
        "chatwoot_token": chatwoot_token,
        "partial_name": partial_name
    }
    return templates.TemplateResponse(request=request, name="preview.html", context=context)

@router.get("/")
async def root(request: Request, contenido: ContenidoModel = Depends(get_contenido), chatwoot_token: str = Depends(get_chatwoot_token)):
    context: Dict[str, Any] = {
        "brand": contenido.brand.model_dump(),
        "content": contenido.content.model_dump(),
        "seo": contenido.seo.model_dump(),
        "chatwoot_token": chatwoot_token
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)
