### Validación de Datos con Pydantic V2 en FastAPI

Pydantic es la librería de validación y parsing de datos líder en Python y constituye el corazón del ecosistema de FastAPI. En esta lección aprenderás a definir modelos de datos sólidos para asegurar que la entrada a tus modelos de Ciencia de Datos sea precisa, segura y autocorregible.

---

### 1. Definición de Schemas con `BaseModel` y `Field`

Un schema en Pydantic se construye creando una clase que hereda de `pydantic.BaseModel`. La función `Field` permite especificar metadata, descripciones para OpenAPI y restricciones numéricas o de longitud de texto.

```python
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import List, Optional
from datetime import datetime

class SensorReadingSchema(BaseModel):
    sensor_id: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description="Identificador único del sensor instalado en planta",
        examples=["SNS-TEMP-001"]
    )
    temperatura: float = Field(
        ...,
        gt=-50.0,
        lt=150.0,
        description="Temperatura registrada en grados Celsius"
    )
    presion: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="Presión operativa en Bar"
    )
    unidades: str = "metric"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

---

### 2. Validadores Personalizados (`@field_validator` y `@model_validator`)

Cuando las validaciones estándar de tipo o rango no son suficientes, Pydantic provee decoradores para ejecutar funciones de validación personalizadas:

#### Validar un Campo Individual con `@field_validator`

```python
from pydantic import field_validator

class InferenciaMLInput(BaseModel):
    codigo_modelo: str
    valores_caracteristicas: list[float]

    @field_validator("codigo_modelo")
    @classmethod
    def validar_codigo_modelo(cls, v: str) -> str:
        modelos_permitidos = {"rf_v1", "xgb_v2", "nn_v3"}
        v_clean = v.lower().strip()
        if v_clean not in modelos_permitidos:
            raise ValueError(f"El modelo '{v}' no está permitido. Opciones: {modelos_permitidos}")
        return v_clean
```

#### Validación Cruzada entre Múltiples Campos con `@model_validator`

```python
from pydantic import model_validator

class RangoMedicionSchema(BaseModel):
    val_minimo: float
    val_maximo: float

    @model_validator(mode="after")
    def verificar_rango_coherente(self) -> "RangoMedicionSchema":
        if self.val_minimo >= self.val_maximo:
            raise ValueError("El valor mínimo debe ser estrictamente menor que el valor máximo.")
        return self
```

---

### 3. Configuración de Modelos mediante `ConfigDict`

En Pydantic V2, el comportamiento global del modelo se configura definiendo un objeto `model_config = ConfigDict(...)`:

```python
from pydantic import ConfigDict

class MaquinariaSchema(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,       # Elimina espacios en blanco en strings
        extra="forbid",                   # Rechaza campos no definidos en el JSON de entrada
        from_attributes=True              # Permite la conversión desde ORMs/SQLAlchemy
    )
    
    nombre: str
    numero_serie: str
```

---

### 4. Estructura de Errores HTTP 422 en FastAPI

Si un cliente envía un payload JSON que no cumple con el schema definido en el endpoint, FastAPI interceptará automáticamente el error de Pydantic y devolverá un código HTTP **422 Unprocessable Entity** con un detalle exhaustivo:

```json
{
  "detail": [
    {
      "type": "greater_than",
      "loc": ["body", "temperatura"],
      "msg": "Input should be greater than -50",
      "input": -100.0
    }
  ]
}
```

---

### 5. Ejemplo Práctico: Schema Completo de Predicción para Data Science

```python
from fastapi import FastAPI, status
from pydantic import BaseModel, Field, ConfigDict

app = FastAPI()

class FeaturesPrediccionMantenimiento(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    rpm: float = Field(..., gt=0, le=10000, description="Revoluciones por minuto")
    vibracion_mm_s: float = Field(..., ge=0, le=50.0, description="Vibración RMS en mm/s")
    horas_operacion: int = Field(..., ge=0, description="Horas totales acumuladas")
    tipo_lubricante: str = Field("sintetico", description="Tipo de lubricante usado")

class RespuestaPrediccion(BaseModel):
    probabilidad_falla: float
    categoria_riesgo: str
    requiere_mantenimiento: bool

@app.post("/predict", response_model=RespuestaPrediccion, tags=["ML Inference"])
def predecir_falla(datos: FeaturesPrediccionMantenimiento):
    # Lógica ficticia de cálculo
    score = (datos.vibracion_mm_s / 50.0) * 0.7 + (datos.rpm / 10000.0) * 0.3
    riesgo = "ALTO" if score > 0.6 else "NORMAL"
    
    return RespuestaPrediccion(
        probabilidad_falla=round(score, 4),
        categoria_riesgo=riesgo,
        requiere_mantenimiento=score > 0.6
    )
```

La utilización estricta de schemas Pydantic asegura la calidad de los datos requeridos por los algoritmos de Ciencia de Datos antes de ejecutar cualquier función pesada de cálculo o inferencia.
