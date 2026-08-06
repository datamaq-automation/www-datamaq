from typing import Any, Dict
from pathlib import Path
from fastapi import APIRouter, Request, Depends
from fastapi.responses import FileResponse
from datetime import datetime
from src.infrastructure.settings import config
from src.infrastructure.fastapi.dependencies import templates, get_contenido, get_geografia, get_industrias, get_cursos_service
from src.infrastructure.fastapi.utils.seo import canonical_url
from src.domain.models import ContenidoModel, IndustriaModel
from src.adapters.presenters.content_presenter import present_contenido
from src.application.data_service import DataService

router = APIRouter()

def _content_lastmod() -> str:
    """
    Devuelve la fecha de modificación más reciente de los archivos de datos
    de contenido (YAML/Markdown) para usar como lastmod del sitemap.
    Si no se encuentran archivos, retorna la fecha actual.
    """
    data_dir = Path("data")
    latest_mtime: float = 0.0
    if data_dir.exists():
        for path in data_dir.rglob("*"):
            if path.is_file() and path.suffix.lower() in (".yaml", ".yml", ".md"):
                mtime = path.stat().st_mtime
                if mtime > latest_mtime:
                    latest_mtime = mtime
    if latest_mtime:
        return datetime.fromtimestamp(latest_mtime).strftime("%Y-%m-%d")
    return datetime.now().strftime("%Y-%m-%d")

@router.get("/robots.txt")
async def robots():
    return FileResponse(config.ROBOTS_TXT_PATH)

@router.get("/humans.txt")
async def humans():
    return FileResponse(config.HUMANS_TXT_PATH, media_type="text/plain")

@router.get("/sitemap.xml")
async def sitemap(
    request: Request,
    contenido: ContenidoModel = Depends(get_contenido),
    geografia: Dict[str, Any] = Depends(get_geografia),
    industrias_data: IndustriaModel = Depends(get_industrias),
    cursos_service: DataService = Depends(get_cursos_service)
):
    base_url = "https://datamaq.com.ar"
    lastmod = _content_lastmod()

    urls = [
        {"loc": f"{base_url}/", "lastmod": lastmod, "changefreq": "monthly", "priority": "1.0"},
        {"loc": f"{base_url}/contact", "lastmod": lastmod, "changefreq": "monthly", "priority": "0.6"},
        {"loc": f"{base_url}/terminos-y-condiciones", "lastmod": lastmod, "changefreq": "yearly", "priority": "0.3"},
        {"loc": f"{base_url}/cursos", "lastmod": lastmod, "changefreq": "monthly", "priority": "0.8"},
        {"loc": f"{base_url}/casos", "lastmod": lastmod, "changefreq": "monthly", "priority": "0.8"},
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

    for caso in cursos_service.get_casos():
        urls.append({
            "loc": f"{base_url}/casos/{caso.slug}",
            "lastmod": lastmod,
            "changefreq": "monthly",
            "priority": "0.7",
        })

    return templates.TemplateResponse(
        request=request,
        name="sitemap.xml",
        context={"urls": urls},
        media_type="application/xml"
    )

@router.get("/dev/preview/{partial_name:path}")
async def preview(request: Request, partial_name: str, contenido: ContenidoModel = Depends(get_contenido)):
    presented = present_contenido(contenido)
    context: Dict[str, Any] = {
        "brand": presented["brand"],
        "content": presented["content"],
        "seo": presented["seo"],
        "footer": presented.get("footer"),
        "partial_name": partial_name,
        "config": config
    }
    response = templates.TemplateResponse(request=request, name="preview.html", context=context)
    response.headers["X-Robots-Tag"] = "noindex, nofollow"
    return response

@router.get("/")
async def root(request: Request, contenido: ContenidoModel = Depends(get_contenido)):
    presented = present_contenido(contenido)
    base_seo: Dict[str, Any] = presented["seo"]
    seo: Dict[str, Any] = {
        **base_seo,
        "canonical_url": canonical_url(request.url),
        "og_image_width": 1200,
        "og_image_height": 630,
    }
    context: Dict[str, Any] = {
        "brand": presented["brand"],
        "content": presented["content"],
        "seo": seo,
        "footer": presented.get("footer"),
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)

@router.get("/terminos-y-condiciones")
async def terms(request: Request, contenido: ContenidoModel = Depends(get_contenido)):
    presented = present_contenido(contenido)
    base_seo: Dict[str, Any] = presented["seo"]
    seo: Dict[str, Any] = {
        **base_seo,
        "title": f"{presented['legal_pages']['terms']['title']} | {presented['brand']['brandName']}",
        "description": f"Términos y condiciones de uso del sitio web de {presented['brand']['brandName']}.",
        "canonical_url": canonical_url(request.url),
        "og_image_width": 1200,
        "og_image_height": 630,
    }
    context: Dict[str, Any] = {
        "brand": presented["brand"],
        "content": presented["content"],
        "terms": presented["legal_pages"]["terms"],
        "cookie_banner": presented["content"]["cookie_banner"],
        "seo": seo,
        "footer": presented.get("footer"),
    }
    return templates.TemplateResponse(request=request, name="terms.html", context=context)
