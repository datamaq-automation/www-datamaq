from typing import Any
from pydantic_core import core_schema

class Price(float):
    """Value Object que representa un Precio no negativo en el dominio."""
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.float_schema(),
        )

    @classmethod
    def validate(cls, v: float) -> "Price":
        if v < 0.0:
            raise ValueError(f"Precio inválido: {v}. No puede ser negativo.")
        return cls(v)
