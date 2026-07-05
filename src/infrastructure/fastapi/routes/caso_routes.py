from typing import Any, Dict
from fastapi import APIRouter, Request, HTTPException, Depends
from src.infrastructure.fastapi.dependencies import templates, get_contenido, get_chatwoot_token, get_cursos_service
from src.infrastructure.fastapi.utils.seo import canonical_url
from src.domain.models import ContenidoModel
from src.application.data_service import DataService

router = APIRouter(prefix="/casos", tags=["casos"])


@router.get("")
async def listado_casos(
    request: Request,
    contenido: ContenidoModel = Depends(get_contenido),
    casos_service: DataService = Depends(get_cursos_service),
    chatwoot_token: str = Depends(get_chatwoot_token)
):
    casos = casos_service.get_casos()
    brand_data = contenido.brand.model_dump()
    cases_data = contenido.content.cases.model_dump()

    seo: Dict[str, Any] = {
        "title": f"{cases_data['title']} | {contenido.brand.brandName}",
        "description": cases_data['subtitle'],
        "canonical_url": canonical_url(request.url),
        "site_name": contenido.brand.brandName,
        "og_image": contenido.seo.og_image,
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: Dict[str, Any] = {
        "brand": brand_data,
        "content": contenido.content.model_dump(),
        "cases": cases_data,
        "casos": [c.model_dump() for c in casos],
        "seo": seo,
        "footer": contenido.footer.model_dump() if contenido.footer else None,
        "chatwoot_token": chatwoot_token,
    }
    return templates.TemplateResponse(request=request, name="casos/list.html", context=context)


@router.get("/{caso_slug}")
async def detalle_caso(
    request: Request,
    caso_slug: str,
    contenido: ContenidoModel = Depends(get_contenido),
    casos_service: DataService = Depends(get_cursos_service),
    chatwoot_token: str = Depends(get_chatwoot_token)
):
    caso = casos_service.get_caso_por_slug(caso_slug)
    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")

    brand_data = contenido.brand.model_dump()
    seo: Dict[str, Any] = {
        "title": f"Caso: {caso.title} | {contenido.brand.brandName}",
        "description": caso.summary,
        "canonical_url": canonical_url(request.url),
        "site_name": contenido.brand.brandName,
        "og_image": caso.og_image or contenido.seo.og_image,
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: Dict[str, Any] = {
        "brand": brand_data,
        "content": contenido.content.model_dump(),
        "cases": contenido.content.cases.model_dump(),
        "caso": caso.model_dump(),
        "seo": seo,
        "footer": contenido.footer.model_dump() if contenido.footer else None,
        "chatwoot_token": chatwoot_token,
    }
    return templates.TemplateResponse(request=request, name="casos/detail.html", context=context)
