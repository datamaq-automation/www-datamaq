from typing import Any, Dict
from fastapi import APIRouter, Request, HTTPException, Depends
from src.infrastructure.fastapi.dependencies import templates, get_contenido, get_industrias, get_chatwoot_token
from src.infrastructure.fastapi.utils.seo import canonical_url
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
        "title": f"Asistencia técnica para {nombre_industria} | DataMaq",
        "description": f"Asistencia técnica híbrida para la {nombre_industria}: visitas en campo, consultoría remota y capacitaciones de cortesía sobre monitoreo de energía e IoT industrial.",
        "canonical_url": canonical_url(request.url),
        "site_name": contenido.brand.brandName,
        "og_image": contenido.seo.og_image,
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    hero_title = f"Asistencia técnica para {nombre_industria}"
    hero_subtitle = f"Visitas en campo y asistencia remota adaptadas a la {nombre_industria}. Monitoreo de energía, captura de datos operativos e IoT industrial."

    context: Dict[str, Any] = {
        "brand": brand_data,
        "content": contenido.content.model_dump(),
        "servicios": servicios_data,
        "faq": contenido.content.faq.questions,
        "chatwoot_token": chatwoot_token,
        "industria_nombre": nombre_industria,
        "seo": seo,
        "footer": contenido.footer.model_dump() if contenido.footer else None,
        "hero_title": hero_title,
        "hero_subtitle": hero_subtitle,
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)
