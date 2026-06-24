from typing import Any, Dict
from fastapi import APIRouter, Request, HTTPException, Depends
from src.infrastructure.fastapi.dependencies import templates, get_contenido, get_chatwoot_token, get_cursos_service
from src.infrastructure.fastapi.utils.seo import canonical_url
from src.domain.models import ContenidoModel

router = APIRouter(prefix="/cursos", tags=["cursos"])

@router.get("")
async def listado_cursos(
    request: Request,
    contenido: ContenidoModel = Depends(get_contenido),
    cursos_service = Depends(get_cursos_service),
    chatwoot_token: str = Depends(get_chatwoot_token)
):
    cursos = cursos_service.get_cursos()
    brand_data = contenido.brand.model_dump()
    
    seo = {
        "title": "Cursos y Capacitaciones Técnicas | DataMaq",
        "description": "Formación práctica y gratuita en Python, IoT industrial y captura de datos operativos para ingenieros y técnicos.",
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": contenido.seo.og_image,
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: Dict[str, Any] = {
        "brand": brand_data,
        "content": contenido.content.model_dump(),
        "cursos": [c.model_dump() for c in cursos],
        "seo": seo,
        "chatwoot_token": chatwoot_token,
    }
    return templates.TemplateResponse(request=request, name="cursos/list.html", context=context)


@router.get("/{curso_slug}")
async def detalle_curso(
    request: Request,
    curso_slug: str,
    contenido: ContenidoModel = Depends(get_contenido),
    cursos_service = Depends(get_cursos_service),
    chatwoot_token: str = Depends(get_chatwoot_token)
):
    curso = cursos_service.get_curso_por_slug(curso_slug)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
        
    brand_data = contenido.brand.model_dump()
    seo = {
        "title": f"Curso: {curso.title} | DataMaq",
        "description": curso.description_short,
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": curso.og_image or contenido.seo.og_image,
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: Dict[str, Any] = {
        "brand": brand_data,
        "content": contenido.content.model_dump(),
        "curso": curso.model_dump(),
        "seo": seo,
        "chatwoot_token": chatwoot_token,
    }
    return templates.TemplateResponse(request=request, name="cursos/detail.html", context=context)


@router.get("/{curso_slug}/{leccion_slug}")
async def vista_leccion(
    request: Request,
    curso_slug: str,
    leccion_slug: str,
    contenido: ContenidoModel = Depends(get_contenido),
    cursos_service = Depends(get_cursos_service),
    chatwoot_token: str = Depends(get_chatwoot_token)
):
    resultado = cursos_service.get_leccion(curso_slug, leccion_slug)
    if not resultado:
        raise HTTPException(status_code=404, detail="Lección o curso no encontrado")
        
    curso, leccion = resultado
    brand_data = contenido.brand.model_dump()
    
    seo = {
        "title": f"{leccion.title} - Curso: {curso.title} | DataMaq",
        "description": f"Lección sobre {leccion.title} en el curso {curso.title}. Cursado gratuito en DataMaq.",
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": curso.og_image or contenido.seo.og_image,
        "og_image_width": 1200,
        "og_image_height": 630,
        "meta_robots": "noindex, follow",  # Evita duplicación y canibalización de SEO interno
    }

    # Determinamos lección anterior y siguiente para facilitar la navegación fluida
    prev_lesson = None
    next_lesson = None
    all_lessons = []
    
    for section in curso.sections:
        for item in section.items:
            all_lessons.append(item)
            
    for i, item in enumerate(all_lessons):
        if item.id == leccion.id:
            if i > 0:
                prev_lesson = all_lessons[i - 1]
            if i < len(all_lessons) - 1:
                next_lesson = all_lessons[i + 1]
            break

    context: Dict[str, Any] = {
        "brand": brand_data,
        "content": contenido.content.model_dump(),
        "curso": curso.model_dump(),
        "leccion": leccion.model_dump(),
        "prev_lesson": prev_lesson.model_dump() if prev_lesson else None,
        "next_lesson": next_lesson.model_dump() if next_lesson else None,
        "seo": seo,
        "chatwoot_token": chatwoot_token,
    }
    return templates.TemplateResponse(request=request, name="cursos/lesson.html", context=context)
