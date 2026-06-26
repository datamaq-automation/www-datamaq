from typing import Any, Dict, List, Union
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from src.infrastructure.fastapi.dependencies import templates, get_contenido, get_chatwoot_token, get_cursos_service
from src.infrastructure.fastapi.utils.seo import canonical_url
from src.domain.models import ContenidoModel, LessonModel, QuizModel
from src.application.data_service import DataService

router = APIRouter(prefix="/cursos", tags=["cursos"])

@router.get("")
async def listado_cursos(
    request: Request,
    contenido: ContenidoModel = Depends(get_contenido),
    cursos_service: DataService = Depends(get_cursos_service),
    chatwoot_token: str = Depends(get_chatwoot_token)
):
    cursos = cursos_service.get_cursos()
    brand_data = contenido.brand.model_dump()
    
    seo: Dict[str, Any] = {
        "title": "Cursos y Capacitaciones Técnicas | DataMaq",
        "description": "Formación práctica y gratuita en Python, IoT industrial y captura de datos operativos para ingenieros y técnicos.",
        "canonical_url": canonical_url(request.url),
        "site_name": contenido.brand.brandName,
        "og_image": contenido.seo.og_image,
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: Dict[str, Any] = {
        "brand": brand_data,
        "content": contenido.content.model_dump(),
        "cursos": [c.model_dump() for c in cursos],
        "seo": seo,
        "footer": contenido.footer.model_dump() if contenido.footer else None,
        "chatwoot_token": chatwoot_token,
    }
    return templates.TemplateResponse(request=request, name="cursos/list.html", context=context)


@router.get("/instructor")
@router.get("/instructor/")
async def redireccionar_instructor_por_defecto(
    cursos_service: DataService = Depends(get_cursos_service)
):
    instructores = list(cursos_service.get_instructores_dict().values())
    if not instructores:
        raise HTTPException(status_code=404, detail="No se encontraron instructores")
    default_id = instructores[0].id
    return RedirectResponse(url=f"/cursos/instructor/{default_id}", status_code=307)


@router.get("/instructor/{instructor_id}")
async def detalle_instructor(
    request: Request,
    instructor_id: str,
    contenido: ContenidoModel = Depends(get_contenido),
    cursos_service: DataService = Depends(get_cursos_service),
    chatwoot_token: str = Depends(get_chatwoot_token)
):
    instructor = cursos_service.get_instructor_por_id(instructor_id)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor no encontrado")

    # Obtener cursos dictados por este instructor
    cursos = [c for c in cursos_service.get_cursos() if c.instructor.id == instructor_id]
    brand_data = contenido.brand.model_dump()

    seo: Dict[str, Any] = {
        "title": f"Instructor: {instructor.name} | DataMaq",
        "description": instructor.bio[:150],
        "canonical_url": canonical_url(request.url),
        "site_name": contenido.brand.brandName,
        "og_image": instructor.photo,
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: Dict[str, Any] = {
        "brand": brand_data,
        "content": contenido.content.model_dump(),
        "instructor": instructor.model_dump(),
        "cursos": [c.model_dump() for c in cursos],
        "seo": seo,
        "footer": contenido.footer.model_dump() if contenido.footer else None,
        "chatwoot_token": chatwoot_token,
    }
    return templates.TemplateResponse(request=request, name="cursos/instructor.html", context=context)


@router.get("/{curso_slug}")
async def detalle_curso(
    request: Request,
    curso_slug: str,
    contenido: ContenidoModel = Depends(get_contenido),
    cursos_service: DataService = Depends(get_cursos_service),
    chatwoot_token: str = Depends(get_chatwoot_token)
):
    curso = cursos_service.get_curso_por_slug(curso_slug)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
        
    brand_data = contenido.brand.model_dump()
    seo: Dict[str, Any] = {
        "title": f"Curso: {curso.title} | DataMaq",
        "description": curso.description_short,
        "canonical_url": canonical_url(request.url),
        "site_name": contenido.brand.brandName,
        "og_image": curso.og_image or contenido.seo.og_image,
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: Dict[str, Any] = {
        "brand": brand_data,
        "content": contenido.content.model_dump(),
        "curso": curso.model_dump(),
        "seo": seo,
        "footer": contenido.footer.model_dump() if contenido.footer else None,
        "chatwoot_token": chatwoot_token,
    }
    return templates.TemplateResponse(request=request, name="cursos/detail.html", context=context)


@router.get("/{curso_slug}/{leccion_slug}")
async def vista_leccion(
    request: Request,
    curso_slug: str,
    leccion_slug: str,
    contenido: ContenidoModel = Depends(get_contenido),
    cursos_service: DataService = Depends(get_cursos_service),
    chatwoot_token: str = Depends(get_chatwoot_token)
):
    resultado = cursos_service.get_leccion(curso_slug, leccion_slug)
    if not resultado:
        raise HTTPException(status_code=404, detail="Lección o curso no encontrado")
        
    curso, leccion = resultado
    brand_data = contenido.brand.model_dump()
    
    seo: Dict[str, Any] = {
        "title": f"{leccion.title} - Curso: {curso.title} | DataMaq",
        "description": f"Lección sobre {leccion.title} en el curso {curso.title}. Cursado gratuito en DataMaq.",
        "canonical_url": canonical_url(request.url),
        "site_name": contenido.brand.brandName,
        "og_image": curso.og_image or contenido.seo.og_image,
        "og_image_width": 1200,
        "og_image_height": 630,
        "meta_robots": "noindex, follow",
    }

    # Determinamos lección anterior y siguiente para facilitar la navegación fluida
    prev_lesson = None
    next_lesson = None
    all_lessons: List[Union[LessonModel, QuizModel]] = []
    
    for section in curso.sections:
        for chapter in section.chapters:
            for item in chapter.items:
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
        "footer": contenido.footer.model_dump() if contenido.footer else None,
        "chatwoot_token": chatwoot_token,
    }
    return templates.TemplateResponse(request=request, name="cursos/lesson.html", context=context)

