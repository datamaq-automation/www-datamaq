from typing import Any, Dict, List, Optional, Tuple, Union, cast
from src.domain.models import ContenidoModel, IndustriaModel, CursosContainerModel, CourseModel, LessonModel, QuizModel, InstructorModel, InstructoresContainerModel
import yaml

class DataService:
    def __init__(self, content_path: str, geography_path: str, industry_path: str, courses_dir: str, instructors_path: str):
        self.content_path = content_path
        self.geography_path = geography_path
        self.industry_path = industry_path
        self.courses_dir = courses_dir
        self.instructors_path = instructors_path
        self._cached_cursos: Optional[CursosContainerModel] = None
        self._cached_instructores: Optional[Dict[str, InstructorModel]] = None

    def get_contenido(self) -> ContenidoModel:
        with open(self.content_path, "r", encoding="utf-8") as f:
            raw_data: Dict[str, Any] = yaml.safe_load(f) # type: ignore
            
            # Populate calculated fields
            if 'content' in raw_data and 'services' in raw_data['content'] and 'cards' in raw_data['content']['services']:
                for card in raw_data['content']['services']['cards']:
                    if 'title' in card:
                        card['cta'] = f"Consultá por {card['title'].split(' ')[0]}"
            
            return ContenidoModel(**raw_data)

    def get_geografia(self) -> Dict[str, Any]:
        with open(self.geography_path, "r", encoding="utf-8") as f:
            return cast(Dict[str, Any], yaml.safe_load(f)) # type: ignore

    def get_industrias(self) -> IndustriaModel:
        with open(self.industry_path, "r", encoding="utf-8") as f:
            raw_data: Dict[str, Any] = yaml.safe_load(f) # type: ignore
            return IndustriaModel(**raw_data)

    def get_cursos_container(self) -> CursosContainerModel:
        if self._cached_cursos is None:
            import os
            import markdown
            
            cursos_list = []
            md_extensions = ["fenced_code", "tables"]
            instructores = self.get_instructores_dict()
            
            if os.path.exists(self.courses_dir):
                for folder_name in sorted(os.listdir(self.courses_dir)):
                    curso_folder_path = os.path.join(self.courses_dir, folder_name)
                    if os.path.isdir(curso_folder_path):
                        curso_yaml_path = os.path.join(curso_folder_path, "curso.yaml")
                        if os.path.exists(curso_yaml_path):
                            with open(curso_yaml_path, "r", encoding="utf-8") as f:
                                curso_data: Dict[str, Any] = yaml.safe_load(f) or {}
                                
                                # Popular instructor desde el repositorio de instructores
                                instructor_id = curso_data.get("instructor_id")
                                if instructor_id in instructores:
                                    curso_data["instructor"] = instructores[instructor_id].model_dump()
                                else:
                                    # Fallback seguro
                                    curso_data["instructor"] = {
                                        "id": "unknown",
                                        "name": "Desconocido",
                                        "role": "Instructor",
                                        "photo": "/static/media/tecnico-a-cargo.webp",
                                        "bio": "Instructor de Datamaq"
                                    }
                                
                                # Cargar lecciones markdown locales al curso
                                if "sections" in curso_data:
                                    for seccion in curso_data["sections"]:
                                        if "chapters" in seccion:
                                            for chapter in seccion["chapters"]:
                                                if "items" in chapter:
                                                    for item in chapter["items"]:
                                                        if item.get("type") == "lesson" and item.get("content_file"):
                                                            file_path = os.path.join(curso_folder_path, "lecciones", item["content_file"])
                                                            if os.path.exists(file_path):
                                                                with open(file_path, "r", encoding="utf-8") as cf:
                                                                    raw_markdown = cf.read()
                                                                    item["content"] = markdown.markdown(raw_markdown, extensions=md_extensions)
                                                            else:
                                                                item["content"] = f"<p class='error'>Error: No se encontró el archivo de contenido en {file_path}</p>"
                                
                                cursos_list.append(curso_data)
            
            self._cached_cursos = CursosContainerModel(cursos=cursos_list)
        return self._cached_cursos

    def get_instructores_dict(self) -> Dict[str, InstructorModel]:
        if self._cached_instructores is None:
            with open(self.instructors_path, "r", encoding="utf-8") as f:
                raw_data: Dict[str, Any] = yaml.safe_load(f) or {"instructores": []} # type: ignore
            
            container = InstructoresContainerModel(**raw_data)
            self._cached_instructores = {inst.id: inst for inst in container.instructores}
        return self._cached_instructores

    def get_cursos(self) -> List[CourseModel]:
        return self.get_cursos_container().cursos

    def get_curso_por_slug(self, slug: str) -> Optional[CourseModel]:
        for curso in self.get_cursos():
            if curso.slug == slug:
                return curso
        return None

    def get_leccion(self, curso_slug: str, leccion_slug: str) -> Optional[Tuple[CourseModel, Union[LessonModel, QuizModel]]]:
        curso = self.get_curso_por_slug(curso_slug)
        if not curso:
            return None
        for seccion in curso.sections:
            for chapter in seccion.chapters:
                for item in chapter.items:
                    if item.slug == leccion_slug:
                        return curso, item
        return None

    def get_instructor_por_id(self, instructor_id: str) -> Optional[InstructorModel]:
        return self.get_instructores_dict().get(instructor_id)

