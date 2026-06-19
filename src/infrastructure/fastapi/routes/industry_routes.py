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
        "title": f"Electricista especializado en {nombre_industria} - Urgencias 24/7",
        "description": f"\u00bfNecesit\u00e1s un electricista en {nombre_industria}? Servicio profesional certificado en {industria_formateada}. Atenci\u00f3n r\u00e1pida, segura y 24/7.",
        "canonical_url": str(request.url),
        "site_name": contenido.brand.brandName,
        "og_image": contenido.seo.og_image,
    }

    context: Dict[str, Any] = {
        "brand": brand_data,
        "content": contenido.content.model_dump(),
        "servicios": servicios_data,
        "faq": contenido.content.faq.questions,
        "chatwoot_token": chatwoot_token,
        "industria_nombre": nombre_industria,
        "seo": seo,
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)
