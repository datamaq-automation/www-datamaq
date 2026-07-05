import re
from typing import Any
from pydantic_core import core_schema

class Slug(str):
    """Value Object que representa un Slug url-safe e inmutable en el dominio."""
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
        )

    @classmethod
    def validate(cls, v: str) -> "Slug":
        if not re.match(r"^[a-z0-9-]+$", v):
            raise ValueError(f"Slug inválido: '{v}'. Debe ser alfanumérico en minúsculas con guiones.")
        return cls(v)
