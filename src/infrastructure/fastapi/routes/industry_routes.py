from typing import Any, Dict
from fastapi import APIRouter, Request, HTTPException, Depends
from src.infrastructure.fastapi.dependencies import templates, get_contenido, get_industrias, get_chatwoot_token
from src.infrastructure.fastapi.schemas import ContenidoModel, IndustriaModel

router = APIRouter()

@router.get("/industria/{industria}.html")
async def pagina_industria(request: Request, industria: str, contenido: ContenidoModel = Depends(get_contenido), industrias_data: IndustriaModel = Depends(get_industrias), chatwoot_token: str = Depends(get_chatwoot_token)):
    
    nombre_industria = industrias_data.industrias.get(industria)
    
    if not nombre_industria:
        raise HTTPException(status_code=404, detail="Industria no encontrada")
        
    context: Dict[str, Any] = {
        "negocio": contenido.negocio.model_dump(),
        "servicios": [s.model_dump() for s in contenido.servicios],
        "faq": contenido.faq,
        "chatwoot_token": chatwoot_token,
        "industria_nombre": nombre_industria,
        "seo_titulo": f"Electricista especializado en {nombre_industria} - Urgencias 24/7",
        "seo_descripcion": f"¿Necesitas soluciones eléctricas para {nombre_industria}? Servicio profesional certificado, rápido y seguro. Atención 24/7."
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)
