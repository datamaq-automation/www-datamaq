from typing import Any, Dict
from fastapi import APIRouter, Request, HTTPException, Depends
from src.infrastructure.fastapi.dependencies import templates, get_contenido, get_geografia, get_chatwoot_token
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
        "title": f"Captura de datos operativos en {nombre_localidad}, {municipio_formateado} | DataMaq",
        "description": f"Soluciones de captura autom\u00e1tica de datos operativos, energ\u00eda y producci\u00f3n en {nombre_localidad}. Asesoramiento t\u00e9cnico e implementaci\u00f3n IoT.",
        "canonical_url": str(request.url),
        "site_name": contenido.brand.brandName,
        "og_image": contenido.seo.og_image,
    }

    hero_title = f"Captura de datos operativos en {nombre_localidad}"
    hero_subtitle = f"Implementaci\u00f3n t\u00e9cnica de equipos IoT para medir energ\u00eda y variables de producci\u00f3n en {nombre_localidad}, {municipio_formateado}."

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
        "hero_title": hero_title,
        "hero_subtitle": hero_subtitle,
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)
