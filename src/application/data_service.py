from typing import Any, Dict, List, Optional, Tuple, Union, cast
from src.domain.models import ContenidoModel, IndustriaModel, CursosContainerModel, CourseModel, LessonModel, QuizModel
import yaml

class DataService:
    def __init__(self, content_path: str, geography_path: str, industry_path: str, courses_path: str):
        self.content_path = content_path
        self.geography_path = geography_path
        self.industry_path = industry_path
        self.courses_path = courses_path
        self._cached_cursos: Optional[CursosContainerModel] = None

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
            with open(self.courses_path, "r", encoding="utf-8") as f:
                raw_data: Dict[str, Any] = yaml.safe_load(f) or {"cursos": []} # type: ignore
                
                import os
                import markdown
                courses_dir = os.path.dirname(self.courses_path)
                md_extensions = ["fenced_code", "tables"]
                
                if "cursos" in raw_data:
                    for curso in raw_data["cursos"]:
                        if "sections" in curso:
                            for seccion in curso["sections"]:
                                if "chapters" in seccion:
                                    for chapter in seccion["chapters"]:
                                        if "items" in chapter:
                                            for item in chapter["items"]:
                                                if item.get("type") == "lesson" and item.get("content_file"):
                                                    file_path = os.path.join(courses_dir, "cursos_contenido", item["content_file"])
                                                    if os.path.exists(file_path):
                                                        with open(file_path, "r", encoding="utf-8") as cf:
                                                            raw_markdown = cf.read()
                                                            item["content"] = markdown.markdown(raw_markdown, extensions=md_extensions)
                                                    else:
                                                        item["content"] = f"<p class='error'>Error: No se encontró el archivo de contenido en {file_path}</p>"
                
                self._cached_cursos = CursosContainerModel(**raw_data)
        return self._cached_cursos

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
