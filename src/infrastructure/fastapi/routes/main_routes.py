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

@router.get("/dev/preview/{partial_name:path}")
async def preview(request: Request, partial_name: str, contenido: ContenidoModel = Depends(get_contenido), chatwoot_token: str = Depends(get_chatwoot_token)):
    context: Dict[str, Any] = {
        "brand": contenido.brand.model_dump(),
        "content": contenido.content.model_dump(),
        "seo": contenido.seo.model_dump(),
        "chatwoot_token": chatwoot_token,
        "partial_name": partial_name
    }
    response = templates.TemplateResponse(request=request, name="preview.html", context=context)
    response.headers["X-Robots-Tag"] = "noindex, nofollow"
    return response

@router.get("/")
async def root(request: Request, contenido: ContenidoModel = Depends(get_contenido), chatwoot_token: str = Depends(get_chatwoot_token)):
    context: Dict[str, Any] = {
        "brand": contenido.brand.model_dump(),
        "content": contenido.content.model_dump(),
        "seo": contenido.seo.model_dump(),
        "chatwoot_token": chatwoot_token
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)

@router.get("/terminos-y-condiciones")
async def terms(request: Request, contenido: ContenidoModel = Depends(get_contenido), chatwoot_token: str = Depends(get_chatwoot_token)):
    base_seo = contenido.seo.model_dump()
    seo = {
        **base_seo,
        "title": f"{contenido.legal_pages.terms.title} | {contenido.brand.brandName}",
        "description": f"T\u00e9rminos y condiciones de uso del sitio web de {contenido.brand.brandName}.",
        "canonical_url": str(request.url),
    }
    context: Dict[str, Any] = {
        "brand": contenido.brand.model_dump(),
        "terms": contenido.legal_pages.terms.model_dump(),
        "cookie_banner": contenido.content.cookie_banner.model_dump(),
        "seo": seo,
        "chatwoot_token": chatwoot_token
    }
    return templates.TemplateResponse(request=request, name="terms.html", context=context)
