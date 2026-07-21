### 3.3 Parámetros de Consulta y Validaciones (Query Parameters & Advanced Validation)

Los **parámetros de consulta** (*Query Parameters*) se envían en la URL a continuación del signo `?` y son esenciales para filtrar, paginar, ordenar y configurar la respuesta de los endpoints en FastAPI.

---

### 1. Definición y Valores por Defecto

Cualquier argumento de función que no esté en la ruta URL es interpretado por FastAPI como un *Query Parameter*.

```python
from fastapi import FastAPI

app = FastAPI(title="API de Parámetros de Consulta")

@app.get("/lecturas")
def obtener_lecturas(
    planta: str = "Avellaneda",  # Opcional con valor por defecto
    max_registros: int = 10,     # Opcional con valor por defecto
    activo: bool = True          # Opcional booleano
):
    return {
        "planta": planta,
        "limite": max_registros,
        "activo": activo
    }
```

---

### 2. Validación Avanzada con `Query()` (Advanced Validation)

Al igual que con `Path()`, la función `Query()` nos permite aplicar metadatos, validaciones de longitud, restricciones numéricas, alias y deprecación de parámetros.

#### Parámetros Principales de `Query()`:
- `min_length` / `max_length`: Restricciones de longitud para cadenas.
- `pattern` (o `regex`): Expresión regular para validar formato.
- `ge`, `gt`, `le`, `lt`: Restricciones numéricas.
- `alias`: Permite declarar un nombre de parámetro en la URL con caracteres no válidos en identificadores de Python (ej. `alias="user-id"` o `alias="order_by"`).
- `deprecated`: Marca el parámetro como obsoleto en la documentación OpenAPI (`deprecated=True`).

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/telemetria/buscar")
def buscar_telemetria(
    query_search: str = Query(
        ...,  # '...' indica que el parámetro es OBLIGATORIO
        alias="q",
        title="Término de Búsqueda",
        description="Palabra clave del sensor o equipo a buscar (min 3 caracteres)",
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_-]+$"
    ),
    pagina: int = Query(
        default=1,
        title="Número de Página",
        ge=1,
        le=500
    ),
    filtro_obsoleto: str | None = Query(
        default=None,
        alias="old-filter",
        deprecated=True,
        description="Parámetro obsoleto. Utilice 'q' en su lugar."
    )
):
    return {
        "busqueda": query_search,
        "pagina": pagina,
        "filtro_obsoleto": filtro_obsoleto
    }
```

#### Ejemplo de Invocación HTTP:
`GET /telemetria/buscar?q=motor_01&pagina=2` $\rightarrow$ **200 OK**.

---

### 3. Parámetros de Consulta con Múltiples Valores (List Query Parameters)

FastAPI permite recibir múltiples valores para una misma clave en la URL (ejemplo: `/sensores?tags=temp&tags=presion&tags=vib`):

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/sensores/filtrar")
def filtrar_por_etiquetas(
    tags: list[str] = Query(
        default=["temperatura", "presion"],
        title="Lista de Etiquetas",
        description="Permite enviar múltiples parámetros ?tags=val1&tags=val2"
    )
):
    return {
        "etiquetas_recibidas": tags,
        "total_filtros": len(tags)
    }
```

#### Ejemplo de Invocación HTTP:
`GET /sensores/filtrar?tags=vibracion&tags=corriente&tags=voltaje`

*Respuesta JSON:*
```json
{
  "etiquetas_recibidas": ["vibracion", "corriente", "voltaje"],
  "total_filtros": 3
}
```

---

### Resumen de la Lección
La función `Query()` ofrece control absoluto sobre los parámetros enviados en la consulta URL: desde requerir parámetros obligatorios con `...`, pasando por aliases como `alias="user-id"`, hasta aceptar listas de múltiples valores.
