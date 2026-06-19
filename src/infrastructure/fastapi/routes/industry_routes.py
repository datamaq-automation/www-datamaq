from typing import Any, Dict
from fastapi import APIRouter, Request, HTTPException, Depends
from src.infrastructure.fastapi.dependencies import templates, get_contenido, get_industrias, get_chatwoot_token
from src.domain.models import ContenidoModel, IndustriaModel

router = APIRouter()

@router.get("/industria/{industria}.html")
async def pagina_industria(request: Request, industria: str, contenido: ContenidoModel = Depends(get_contenido), industrias_data: IndustriaModel = Depends(get_industrias), chatwoot_token: str = Depends(get_chatwoot_token)):
    
    nombre_industria = industrias_data.industrias.get(industria)
    
    if not nombre_industria:
        raise HTTPException(status_code=404, detail="Industria no encontrada")
    
    brand_data = contenido.brand.model_dump()
    servicios_data = [s.model_dump() for s in contenido.content.services.cards]
    industria_formateada = industria.replace("-", " ").title()

    seo = {
        "title": f"Soluciones IoT para {nombre_industria} | DataMaq",
        "description": f"Captura e integraci\u00f3n de datos operativos para la {nombre_industria}. Asesoramiento t\u00e9cnico especializado en energ\u00eda y producci\u00f3n.",
        "canonical_url": str(request.url),
        "site_name": contenido.brand.brandName,
        "og_image": contenido.seo.og_image,
    }

    hero_title = f"Captura de datos para {nombre_industria}"
    hero_subtitle = f"Soluciones de captura autom\u00e1tica de datos operativos, energ\u00eda y producci\u00f3n adaptadas a la {nombre_industria}."

    context: Dict[str, Any] = {
        "brand": brand_data,
        "content": contenido.content.model_dump(),
        "servicios": servicios_data,
        "faq": contenido.content.faq.questions,
        "chatwoot_token": chatwoot_token,
        "industria_nombre": nombre_industria,
        "seo": seo,
        "hero_title": hero_title,
        "hero_subtitle": hero_subtitle,
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)
