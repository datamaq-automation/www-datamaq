### 3.2 Parámetros de Ruta y Validaciones Avanzadas (Path Parameters & Advanced Validation)

En FastAPI, la gestión de parámetros de solicitud (*Request Parameters*) combina las anotaciones de tipo nativas de Python con herramientas de validación avanzada como `Path()` y enumeraciones `Enum`.

---

### 1. Manejo General de Parámetros de Solicitud (Handling Request Parameters)

Cuando una petición HTTP llega a un endpoint de FastAPI, el framework inspecciona automáticamente:
1. Las **variables de ruta** definidas en el template de la URL (ejemplo: `/equipos/{equipo_id}`).
2. Los **argumentos de la función controladora** y sus anotaciones de tipo.
3. Las restricciones numéricas y de formato especificadas mediante metadatos.

Si los datos enviados por el cliente no cumplen con las reglas declaradas, FastAPI detiene la ejecución inmediatamente y retorna un código HTTP **422 Unprocessable Entity** detallando exactamente qué parámetro falló y por qué.

---

### 2. Parámetros de Ruta (Path Parameters)

Los **parámetros de ruta** forman parte de la estructura de la URL y se declaran encerrando la variable entre llaves `{}`.

```python
from fastapi import FastAPI, HTTPException, status

app = FastAPI(title="API de Diagnóstico de Equipos")

equipos_db = {
    101: {"nombre": "Compresor Principal", "vibracion": 0.05},
    102: {"nombre": "Bomba de Agua B2", "vibracion": 0.12}
}

@app.get("/equipos/{equipo_id}")
def obtener_equipo(equipo_id: int):
    if equipo_id not in equipos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipo ID {equipo_id} no encontrado."
        )
    return equipos_db[equipo_id]
```

---

### 3. Limitación de Valores Permitidos (Limiting Allowed Values con Enums)

Para limitar los valores aceptados por un parámetro de ruta a un conjunto predefinido y cerrado de opciones, utilizamos subclases de `str` y `Enum`:

```python
from enum import Enum

class CategoriaEquipo(str, Enum):
    BOMBA = "bomba"
    COMPRESOR = "compresor"
    TURBINA = "turbina"

@app.get("/equipos/categoria/{categoria}")
def obtener_equipos_por_categoria(categoria: CategoriaEquipo):
    """
    Solamente acepta los valores: 'bomba', 'compresor' o 'turbina'.
    Cualquier otro valor generará automáticamente una respuesta 422.
    """
    if categoria is CategoriaEquipo.BOMBA:
        return {"categoria": categoria, "items": ["Bomba Centrífuga A1", "Bomba B2"]}
    return {"categoria": categoria, "items": []}
```

---

### 4. Validación Avanzada con `Path()` (Advanced Validation)

La función `Path()` de FastAPI permite agregar restricciones numéricas, expresiones regulares (regex) y metadatos explicativos para la documentación OpenAPI.

#### Validaciones Numéricas Comunes:
- `ge` (*Greater than or equal*): Mayor o igual que ($\ge$).
- `gt` (*Greater than*): Estrictamente mayor que ($>$).
- `le` (*Less than or equal*): Menor o igual que ($\le$).
- `lt` (*Less than*): Estrictamente menor que ($<$).

#### Validaciones de Texto y Expresiones Regulares:
- `min_length` / `max_length`: Longitud mínima y máxima de caracteres.
- `pattern` (o `regex`): Patrón de expresión regular que debe cumplir la cadena.

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/planta/{codigo_planta}/sensor/{sensor_id}")
def obtener_sensor_avanzado(
    codigo_planta: str = Path(
        ...,
        title="Código de Planta Industrial",
        description="Debe coincidir con el formato AR-PLT-XXX (ej. AR-PLT-001)",
        pattern=r"^AR-PLT-\d{3}$",
        example="AR-PLT-001"
    ),
    sensor_id: int = Path(
        ...,
        title="ID del Sensor",
        description="Identificador numérico entero positivo entre 1 y 9999",
        ge=1,
        le=9999
    )
):
    return {
        "planta": codigo_planta,
        "sensor_id": sensor_id,
        "status": "monitoreado"
    }
```

#### Ejemplo de Invocaciones:
- `GET /planta/AR-PLT-001/sensor/50` $\rightarrow$ **200 OK** (Cumple todas las validaciones).
- `GET /planta/PLANT-A/sensor/50` $\rightarrow$ **422 Unprocessable Entity** (Falla el regex `pattern`).
- `GET /planta/AR-PLT-001/sensor/0` $\rightarrow$ **422 Unprocessable Entity** (Falla `ge=1`).

---

### Resumen de la Lección
Al combinar anotaciones de tipo con `Enum` y las validaciones avanzadas de `Path()`, FastAPI garantiza que los parámetros de ruta cumplan estrictamente con las reglas de negocio antes de ejecutar la lógica del controlador.
