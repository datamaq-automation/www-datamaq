from typing import Any, Dict, cast
from src.domain.models import ContenidoModel, IndustriaModel
import yaml

class DataService:
    def __init__(self, content_path: str, geography_path: str, industry_path: str):
        self.content_path = content_path
        self.geography_path = geography_path
        self.industry_path = industry_path

    def get_contenido(self) -> ContenidoModel:
        with open(self.content_path, "r", encoding="utf-8") as f:
            raw_data: Dict[str, Any] = yaml.safe_load(f) # type: ignore
            return ContenidoModel(**raw_data)

    def get_geografia(self) -> Dict[str, Any]:
        with open(self.geography_path, "r", encoding="utf-8") as f:
            return cast(Dict[str, Any], yaml.safe_load(f)) # type: ignore

    def get_industrias(self) -> IndustriaModel:
        with open(self.industry_path, "r", encoding="utf-8") as f:
            raw_data: Dict[str, Any] = yaml.safe_load(f) # type: ignore
            return IndustriaModel(**raw_data)
