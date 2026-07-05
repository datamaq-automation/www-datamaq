from typing import Any, Dict
from fastapi import APIRouter, Request, HTTPException, Depends
from src.infrastructure.fastapi.dependencies import templates, get_contenido, get_geografia, get_chatwoot_token, get_landing_content
from src.infrastructure.fastapi.utils.seo import canonical_url
from src.domain.models import ContenidoModel, LandingContentModel
from src.adapters.presenters.content_presenter import present_contenido

router = APIRouter()

@router.get("/{provincia}/{municipio}/{localidad}.html")
async def pagina_localidad(request: Request, provincia: str, municipio: str, localidad: str, contenido: ContenidoModel = Depends(get_contenido), geografia: Dict[str, Any] = Depends(get_geografia), landing_content: LandingContentModel = Depends(get_landing_content), chatwoot_token: str = Depends(get_chatwoot_token)):
    # Validar existencia
    locs: Dict[str, Any] = geografia.get("localidades", {})
    prov = locs.get(provincia, {})
    mun = prov.get(municipio, {})
    nombre_localidad = mun.get(localidad)

    if not nombre_localidad:
        raise HTTPException(status_code=404, detail="Localidad no encontrada")

    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]
    servicios_data = content_data["services"]["cards"]
    
    municipio_formateado = municipio.replace("-", " ").title()

    localidad_content = (
        landing_content.localidades
        .get(provincia, {})
        .get(municipio, {})
        .get(localidad)
    )

    seo = {
        "title": f"Asistencia técnica en {nombre_localidad}, {municipio_formateado} | DataMaq",
        "description": f"Visitas técnicas en campo y asistencia remota para monitoreo de energía industrial e IoT en {nombre_localidad}. Capacitaciones de cortesía según el proyecto.",
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    hero_title = f"Asistencia técnica en {nombre_localidad}"
    hero_subtitle = f"Visitas en campo y consultoría remota para monitoreo de energía, captura de datos operativos e IoT industrial en {nombre_localidad}, {municipio_formateado}."

    context: Dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "servicios": servicios_data,
        "faq": content_data["faq"]["questions"],
        "chatwoot_token": chatwoot_token,
        "localidad_nombre": nombre_localidad,
        "municipio": municipio_formateado,
        "provincia": provincia.replace("-", " ").title(),
        "seo": seo,
        "footer": presented.get("footer"),
        "hero_title": hero_title,
        "hero_subtitle": hero_subtitle,
        "landing_localidad": localidad_content.model_dump() if localidad_content else None,
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)
