from typing import Any, Dict
from fastapi import APIRouter, Request, HTTPException, Depends
from src.infrastructure.fastapi.dependencies import templates, get_contenido, get_geografia, get_chatwoot_token
from src.infrastructure.fastapi.utils.seo import canonical_url
from src.domain.models import ContenidoModel

router = APIRouter()

@router.get("/{provincia}/{municipio}/{localidad}.html")
async def pagina_localidad(request: Request, provincia: str, municipio: str, localidad: str, contenido: ContenidoModel = Depends(get_contenido), geografia: Dict[str, Any] = Depends(get_geografia), chatwoot_token: str = Depends(get_chatwoot_token)):
    # Validar existencia
    locs: Dict[str, Any] = geografia.get("localidades", {}) # type: ignore
    prov = locs.get(provincia, {})
    mun = prov.get(municipio, {})
    nombre_localidad = mun.get(localidad)

    if not nombre_localidad:
        raise HTTPException(status_code=404, detail="Localidad no encontrada")

    brand_data = contenido.brand.model_dump()
    servicios_data = [s.model_dump() for s in contenido.content.services.cards]
    municipio_formateado = municipio.replace("-", " ").title()

    seo = {
        "title": f"Monitoreo de energía industrial en {nombre_localidad}, {municipio_formateado} | DataMaq",
        "description": f"Captura de datos operativos y monitoreo de energía industrial en {nombre_localidad}. Soluciones IoT para plantas y procesos productivos.",
        "canonical_url": canonical_url(request.url),
        "site_name": contenido.brand.brandName,
        "og_image": contenido.seo.og_image,
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    hero_title = f"Monitoreo de energía industrial en {nombre_localidad}"
    hero_subtitle = f"Implementaci\u00f3n de equipos IoT para medici\u00f3n de energía y captura de datos operativos en {nombre_localidad}, {municipio_formateado}."

    context: Dict[str, Any] = {
        "brand": brand_data,
        "content": contenido.content.model_dump(),
        "servicios": servicios_data,
        "faq": contenido.content.faq.questions,
        "chatwoot_token": chatwoot_token,
        "localidad_nombre": nombre_localidad,
        "municipio": municipio_formateado,
        "provincia": provincia.replace("-", " ").title(),
        "seo": seo,
        "footer": contenido.footer.model_dump() if contenido.footer else None,
        "hero_title": hero_title,
        "hero_subtitle": hero_subtitle,
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)
