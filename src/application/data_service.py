from typing import Any, Dict, List, Optional, Tuple, Union, cast
from src.domain.models import ContenidoModel, IndustriaModel, LandingContentModel, CasoModel, CasosContainerModel, CursosContainerModel, CourseModel, LessonModel, QuizModel, InstructorModel, InstructoresContainerModel
import yaml # type: ignore
import os

class DataService:
    def __init__(self, content_path: str, geography_path: str, industry_path: str, courses_dir: str, instructors_path: str, redirects_path: str = "", landing_content_path: str = "", cases_dir: str = ""):
        self.content_path = content_path
        self.geography_path = geography_path
        self.industry_path = industry_path
        self.courses_dir = courses_dir
        self.instructors_path = instructors_path
        self.redirects_path = redirects_path
        self.landing_content_path = landing_content_path
        self.cases_dir = cases_dir

        self._cached_contenido: Optional[ContenidoModel] = None
        self._cached_geografia: Optional[Dict[str, Any]] = None
        self._cached_industrias: Optional[IndustriaModel] = None
        self._cached_cursos: Optional[CursosContainerModel] = None
        self._cached_instructores: Optional[Dict[str, InstructorModel]] = None
        self._cached_redirects: Optional[Dict[str, str]] = None
        self._cached_landing_content: Optional[LandingContentModel] = None
        self._cached_casos: Optional[CasosContainerModel] = None

    def get_contenido(self) -> ContenidoModel:
        if self._cached_contenido is None:
            with open(self.content_path, "r", encoding="utf-8") as f:
                raw_data: Dict[str, Any] = yaml.safe_load(f) or {}
            
            # Populate calculated fields
            if 'content' in raw_data and 'services' in raw_data['content'] and 'cards' in raw_data['content']['services']:
                for card in raw_data['content']['services']['cards']:
                    if 'title' in card:
                        card['cta'] = f"Consultá por {card['title'].split(' ')[0]}"
            
            self._cached_contenido = ContenidoModel(**raw_data)
        return self._cached_contenido

    def get_geografia(self) -> Dict[str, Any]:
        if self._cached_geografia is None:
            with open(self.geography_path, "r", encoding="utf-8") as f:
                self._cached_geografia = yaml.safe_load(f) or {}
        return self._cached_geografia

    def get_industrias(self) -> IndustriaModel:
        if self._cached_industrias is None:
            with open(self.industry_path, "r", encoding="utf-8") as f:
                raw_data: Dict[str, Any] = yaml.safe_load(f) or {}
            self._cached_industrias = IndustriaModel(**raw_data)
        return self._cached_industrias

    def get_cursos_container(self) -> CursosContainerModel:
        if self._cached_cursos is None:
            import os
            import markdown # type: ignore
            
            cursos_list: List[CourseModel] = []
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
                                
                                # Resolución por defecto de og_image si no viene definida
                                if not curso_data.get("og_image") and "slug" in curso_data:
                                    curso_data["og_image"] = f"/static/media/cursos/og-{curso_data['slug']}.webp"
                                
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
                                
                                cursos_list.append(CourseModel.model_validate(curso_data))
            
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

    def get_redirects(self) -> Dict[str, str]:
        if self._cached_redirects is None:
            self._cached_redirects = {}
            if self.redirects_path and os.path.exists(self.redirects_path):
                with open(self.redirects_path, "r", encoding="utf-8") as f:
                    raw_data: Dict[str, Any] = yaml.safe_load(f) or {}
                redirects = raw_data.get("redirects") or {}
                if isinstance(redirects, dict):
                    self._cached_redirects = {str(k): str(v) for k, v in redirects.items()}
        return self._cached_redirects

    def get_landing_content(self) -> LandingContentModel:
        if self._cached_landing_content is None:
            self._cached_landing_content = LandingContentModel()
            if self.landing_content_path and os.path.exists(self.landing_content_path):
                with open(self.landing_content_path, "r", encoding="utf-8") as f:
                    raw_data: Dict[str, Any] = yaml.safe_load(f) or {}
                self._cached_landing_content = LandingContentModel(**raw_data)
        return self._cached_landing_content

    def get_casos_container(self) -> CasosContainerModel:
        if self._cached_casos is None:
            import markdown # type: ignore
            casos_list: List[CasoModel] = []
            md_extensions = ["fenced_code", "tables"]

            if os.path.exists(self.cases_dir):
                for folder_name in sorted(os.listdir(self.cases_dir)):
                    caso_folder_path = os.path.join(self.cases_dir, folder_name)
                    if os.path.isdir(caso_folder_path):
                        caso_yaml_path = os.path.join(caso_folder_path, "caso.yaml")
                        if os.path.exists(caso_yaml_path):
                            with open(caso_yaml_path, "r", encoding="utf-8") as f:
                                caso_data: Dict[str, Any] = yaml.safe_load(f) or {}
                            if caso_data.get("content"):
                                caso_data["content"] = markdown.markdown(caso_data["content"], extensions=md_extensions)
                            if not caso_data.get("og_image"):
                                caso_data["og_image"] = "/static/og-default.jpg"
                            casos_list.append(CasoModel.model_validate(caso_data))

            self._cached_casos = CasosContainerModel(casos=casos_list)
        return self._cached_casos

    def get_casos(self) -> List[CasoModel]:
        return self.get_casos_container().casos

    def get_caso_por_slug(self, slug: str) -> Optional[CasoModel]:
        for caso in self.get_casos():
            if caso.slug == slug:
                return caso
        return None

