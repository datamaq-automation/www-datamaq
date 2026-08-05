from typing import Any, Dict
from src.domain.models import ContenidoModel, CourseModel, CasoModel

def present_contenido(contenido: ContenidoModel) -> Dict[str, Any]:
    """Prepara el modelo de contenido general para su presentación, inyectando CTAs dinámicos."""
    data = contenido.model_dump()
    if 'content' in data and 'services' in data['content'] and 'cards' in data['content']['services']:
        for card in data['content']['services']['cards']:
            if not card.get('cta') and card.get('title'):
                card['cta'] = f"Consultá por {card['title'].split(' ')[0]}"
    return data

def present_course(course: CourseModel) -> Dict[str, Any]:
    """Prepara un curso para su presentación, inyectando og_image y dimensiones por defecto si faltan."""
    data = course.model_dump()
    if not data.get("og_image") and data.get("slug"):
        data["og_image"] = f"/static/media/cursos/og-{data['slug']}.webp"
    # Definir dimensiones OG estándar si no están presentes
    if not data.get("og_image_width"):
        data["og_image_width"] = 1200
    if not data.get("og_image_height"):
        data["og_image_height"] = 630
    return data

def present_caso(caso: CasoModel) -> Dict[str, Any]:
    """Prepara un caso para su presentación, inyectando og_image por defecto si falta."""
    data = caso.model_dump()
    if not data.get("og_image"):
        data["og_image"] = "/static/og-default.webp"
    return data
