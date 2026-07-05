from typing import Any, Dict, List, Optional, Tuple, Union
import yaml  # type: ignore
import os
from src.domain.models import (
    ContenidoModel,
    IndustriaModel,
    LandingContentModel,
    CasoModel,
    CasosContainerModel,
    CursosContainerModel,
    CourseModel,
    LessonModel,
    QuizModel,
    InstructorModel,
    InstructoresContainerModel
)
from src.infrastructure.adapters.markdown_parser import MarkdownParser
from src.application.mappers.course_mapper import to_course_model

class DataService:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        
        # Deducir rutas según la arquitectura física por Bounded Contexts
        self.brand_path = os.path.join(data_dir, "config", "brand.yaml")
        self.footer_path = os.path.join(data_dir, "config", "footer.yaml")
        self.redirects_path = os.path.join(data_dir, "config", "redirects.yaml")
        
        self.home_sections_path = os.path.join(data_dir, "content", "home_sections.yaml")
        self.legal_path = os.path.join(data_dir, "content", "legal.yaml")
        
        self.seo_path = os.path.join(data_dir, "seo", "seo.yaml")
        self.landing_content_path = os.path.join(data_dir, "seo", "landing_content.yaml")
        
        self.geography_path = os.path.join(data_dir, "meta", "geografia.yaml")
        self.industry_path = os.path.join(data_dir, "meta", "industrias.yaml")
        
        self.instructors_path = os.path.join(data_dir, "core", "instructores.yaml")
        self.courses_dir = os.path.join(data_dir, "core", "cursos")
        self.cases_dir = os.path.join(data_dir, "core", "casos")

        self.markdown_parser = MarkdownParser()

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
            # Leer los archivos separados del CMS
            with open(self.brand_path, "r", encoding="utf-8") as f:
                brand_data = yaml.safe_load(f) or {}
                
            with open(self.home_sections_path, "r", encoding="utf-8") as f:
                home_sections_data = yaml.safe_load(f) or {}
                
            with open(self.legal_path, "r", encoding="utf-8") as f:
                legal_data = yaml.safe_load(f) or {}
                
            with open(self.seo_path, "r", encoding="utf-8") as f:
                seo_data = yaml.safe_load(f) or {}
                
            with open(self.footer_path, "r", encoding="utf-8") as f:
                footer_data = yaml.safe_load(f) or {}

            # Reconstruir el diccionario compatible con ContenidoModel
            raw_data = {
                "brand": brand_data,
                "content": home_sections_data,
                "seo": seo_data,
                "legal_pages": legal_data,
                "footer": footer_data
            }
            
            # --- Generar Footer Dinámico ---
            if "navigation_groups" not in raw_data["footer"]:
                raw_data["footer"]["navigation_groups"] = []

            # 1. Grupo de Navegación (mantener o definir por defecto)
            nav_group = None
            for group in raw_data["footer"].get("navigation_groups", []):
                if group.get("title") == "Navegación":
                    nav_group = group
                    break
            
            if not nav_group:
                nav_group = {
                    "title": "Navegación",
                    "links": [
                        {"label": "Inicio", "href": "/"},
                        {"label": "Casos", "href": "/casos"},
                        {"label": "Cursos", "href": "/cursos"},
                        {"label": "Contacto", "href": "/contact"}
                    ]
                }
            
            # 2. Grupo de Cobertura dinámica
            geografia_data = self.get_geografia()
            cobertura_links = []
            localidades = geografia_data.get("localidades", {})
            for provincia_key, provincia in localidades.items():
                for municipio_key, municipio in provincia.items():
                    for localidad_key, nombre_localidad in municipio.items():
                        cobertura_links.append({
                            "label": nombre_localidad,
                            "href": f"/{provincia_key}/{municipio_key}/{localidad_key}.html"
                        })
            
            cobertura_group = {
                "title": "Cobertura",
                "links": cobertura_links
            }
            
            # 3. Grupo de Industrias dinámica
            industrias_data = self.get_industrias()
            industrias_links = []
            for industria_key, nombre_industria in industrias_data.industrias.items():
                label = nombre_industria.replace("Industria ", "")
                industrias_links.append({
                    "label": label,
                    "href": f"/industria/{industria_key}.html"
                })
                
            industrias_group = {
                "title": "Industrias",
                "links": industrias_links
            }
            
            raw_data["footer"]["navigation_groups"] = [nav_group, cobertura_group, industrias_group]
            
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
            cursos_list: List[CourseModel] = []
            instructores = self.get_instructores_dict()
            
            if os.path.exists(self.courses_dir):
                for folder_name in sorted(os.listdir(self.courses_dir)):
                    curso_folder_path = os.path.join(self.courses_dir, folder_name)
                    if os.path.isdir(curso_folder_path):
                        curso_yaml_path = os.path.join(curso_folder_path, "curso.yaml")
                        if os.path.exists(curso_yaml_path):
                            with open(curso_yaml_path, "r", encoding="utf-8") as f:
                                curso_data: Dict[str, Any] = yaml.safe_load(f) or {}
                                
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
                                                                    item["content"] = self.markdown_parser.to_html(raw_markdown)
                                                            else:
                                                                item["content"] = f"<p class='error'>Error: No se encontró el archivo de contenido en {file_path}</p>"
                                
                                # Delegar la hidratación/resolución del instructor al mapper
                                course_model = to_course_model(curso_data, instructores)
                                cursos_list.append(course_model)
            
            self._cached_cursos = CursosContainerModel(cursos=cursos_list)
        return self._cached_cursos

    def get_instructores_dict(self) -> Dict[str, InstructorModel]:
        if self._cached_instructores is None:
            with open(self.instructors_path, "r", encoding="utf-8") as f:
                raw_data: Dict[str, Any] = yaml.safe_load(f) or {"instructores": []}
            
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
            casos_list: List[CasoModel] = []

            if os.path.exists(self.cases_dir):
                for folder_name in sorted(os.listdir(self.cases_dir)):
                    caso_folder_path = os.path.join(self.cases_dir, folder_name)
                    if os.path.isdir(caso_folder_path):
                        caso_yaml_path = os.path.join(caso_folder_path, "caso.yaml")
                        if os.path.exists(caso_yaml_path):
                            with open(caso_yaml_path, "r", encoding="utf-8") as f:
                                caso_data: Dict[str, Any] = yaml.safe_load(f) or {}
                            if caso_data.get("content"):
                                caso_data["content"] = self.markdown_parser.to_html(caso_data["content"])
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
