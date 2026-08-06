from typing import Any, Dict
from fastapi import APIRouter, Request, HTTPException, Depends
from src.infrastructure.fastapi.dependencies import templates, get_contenido, get_industrias, get_landing_content
from src.infrastructure.fastapi.utils.seo import canonical_url
from src.domain.models import ContenidoModel, IndustriaModel, LandingContentModel
from src.adapters.presenters.content_presenter import present_contenido

router = APIRouter()

@router.get("/industria/{industria}.html")
async def pagina_industria(request: Request, industria: str, contenido: ContenidoModel = Depends(get_contenido), industrias_data: IndustriaModel = Depends(get_industrias), landing_content: LandingContentModel = Depends(get_landing_content)):

    nombre_industria = industrias_data.industrias.get(industria)

    if not nombre_industria:
        raise HTTPException(status_code=404, detail="Industria no encontrada")

    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]
    servicios_data = content_data["services"]["cards"]

    industria_content = landing_content.industrias.get(industria)

    seo = {
        "title": f"Asistencia técnica para {nombre_industria} | DataMaq",
        "description": f"Asistencia técnica híbrida para la {nombre_industria}: visitas en campo, consultoría remota y capacitaciones de cortesía sobre monitoreo de energía e IoT industrial.",
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    hero_title = f"Asistencia técnica para {nombre_industria}"
    hero_subtitle = f"Visitas en campo y asistencia remota adaptadas a la {nombre_industria}. Monitoreo de energía, captura de datos operativos e IoT industrial."

    context: Dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "servicios": servicios_data,
        "faq": content_data["faq"]["questions"],
        "industria_nombre": nombre_industria,
        "seo": seo,
        "footer": presented.get("footer"),
        "hero_title": hero_title,
        "hero_subtitle": hero_subtitle,
        "landing_industria": industria_content.model_dump() if industria_content else None,
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)
