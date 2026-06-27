from typing import Any, Dict
from fastapi import APIRouter, Request, Depends
from fastapi.responses import FileResponse
from datetime import datetime
from src.infrastructure.settings import config
from src.infrastructure.fastapi.dependencies import templates, get_contenido, get_geografia, get_industrias, get_chatwoot_token, get_cursos_service
from src.infrastructure.fastapi.utils.seo import canonical_url
from src.domain.models import ContenidoModel, IndustriaModel

router = APIRouter()

@router.get("/robots.txt")
async def robots():
    return FileResponse(config.ROBOTS_TXT_PATH)

@router.get("/sitemap.xml")
async def sitemap(
    request: Request,
    contenido: ContenidoModel = Depends(get_contenido),
    geografia: Dict[str, Any] = Depends(get_geografia),
    industrias_data: IndustriaModel = Depends(get_industrias),
    cursos_service = Depends(get_cursos_service)
):
    base_url = "https://datamaq.com.ar"
    lastmod = datetime.now().strftime("%Y-%m-%d")

    urls = [
        {"loc": f"{base_url}/", "lastmod": lastmod, "changefreq": "monthly", "priority": "1.0"},
        {"loc": f"{base_url}/contact", "lastmod": lastmod, "changefreq": "monthly", "priority": "0.6"},
        {"loc": f"{base_url}/terminos-y-condiciones", "lastmod": lastmod, "changefreq": "yearly", "priority": "0.3"},
        {"loc": f"{base_url}/cursos", "lastmod": lastmod, "changefreq": "monthly", "priority": "0.8"},
    ]

    localidades = geografia.get("localidades", {})
    for provincia_key, provincia in localidades.items():
        for municipio_key, municipio in provincia.items():
            for localidad_key in municipio.keys():
                urls.append({
                    "loc": f"{base_url}/{provincia_key}/{municipio_key}/{localidad_key}.html",
                    "lastmod": lastmod,
                    "changefreq": "monthly",
                    "priority": "0.7",
                })

    for industria_key in industrias_data.industrias.keys():
        urls.append({
            "loc": f"{base_url}/industria/{industria_key}.html",
            "lastmod": lastmod,
            "changefreq": "monthly",
            "priority": "0.7",
        })

    for curso in cursos_service.get_cursos():
        urls.append({
            "loc": f"{base_url}/cursos/{curso.slug}",
            "lastmod": lastmod,
            "changefreq": "monthly",
            "priority": "0.8",
        })

    for instructor_id in cursos_service.get_instructores_dict().keys():
        urls.append({
            "loc": f"{base_url}/cursos/instructor/{instructor_id}",
            "lastmod": lastmod,
            "changefreq": "monthly",
            "priority": "0.5",
        })

    return templates.TemplateResponse(
        request=request,
        name="sitemap.xml",
        context={"urls": urls},
        media_type="application/xml"
    )

@router.get("/dev/preview/{partial_name:path}")
async def preview(request: Request, partial_name: str, contenido: ContenidoModel = Depends(get_contenido), chatwoot_token: str = Depends(get_chatwoot_token)):
    context: Dict[str, Any] = {
        "brand": contenido.brand.model_dump(),
        "content": contenido.content.model_dump(),
        "seo": contenido.seo.model_dump(),
        "footer": contenido.footer.model_dump() if contenido.footer else None,
        "chatwoot_token": chatwoot_token,
        "partial_name": partial_name
    }
    response = templates.TemplateResponse(request=request, name="preview.html", context=context)
    response.headers["X-Robots-Tag"] = "noindex, nofollow"
    return response

@router.get("/")
async def root(request: Request, contenido: ContenidoModel = Depends(get_contenido), chatwoot_token: str = Depends(get_chatwoot_token)):
    base_seo = contenido.seo.model_dump()
    seo = {
        **base_seo,
        "canonical_url": canonical_url(request.url),
        "og_image_width": 1200,
        "og_image_height": 630,
    }
    context: Dict[str, Any] = {
        "brand": contenido.brand.model_dump(),
        "content": contenido.content.model_dump(),
        "seo": seo,
        "footer": contenido.footer.model_dump() if contenido.footer else None,
        "chatwoot_token": chatwoot_token
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)

@router.get("/terminos-y-condiciones")
async def terms(request: Request, contenido: ContenidoModel = Depends(get_contenido), chatwoot_token: str = Depends(get_chatwoot_token)):
    base_seo = contenido.seo.model_dump()
    seo = {
        **base_seo,
        "title": f"{contenido.legal_pages.terms.title} | {contenido.brand.brandName}",
        "description": f"Términos y condiciones de uso del sitio web de {contenido.brand.brandName}.",
        "canonical_url": canonical_url(request.url),
        "og_image_width": 1200,
        "og_image_height": 630,
    }
    context: Dict[str, Any] = {
        "brand": contenido.brand.model_dump(),
        "content": contenido.content.model_dump(),
        "terms": contenido.legal_pages.terms.model_dump(),
        "cookie_banner": contenido.content.cookie_banner.model_dump(),
        "seo": seo,
        "footer": contenido.footer.model_dump() if contenido.footer else None,
        "chatwoot_token": chatwoot_token
    }
    return templates.TemplateResponse(request=request, name="terms.html", context=context)
