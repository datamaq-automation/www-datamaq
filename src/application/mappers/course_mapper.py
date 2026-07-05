from typing import Any, Dict
from src.domain.models import CourseModel, InstructorModel

def to_course_model(curso_data: Dict[str, Any], instructores: Dict[str, InstructorModel]) -> CourseModel:
    """
    Mapea un diccionario crudo de datos de curso a un modelo de dominio CourseModel,
    resolviendo la relación con el instructor correspondiente.
    """
    data = dict(curso_data)
    instructor_id = data.get("instructor_id")
    
    if instructor_id in instructores:
        data["instructor"] = instructores[instructor_id].model_dump()
    else:
        # Fallback seguro
        data["instructor"] = {
            "id": "unknown",
            "name": "Desconocido",
            "role": "Instructor",
            "photo": "/static/media/tecnico-a-cargo.webp",
            "bio": "Instructor de Datamaq"
        }
        
    return CourseModel.model_validate(data)
