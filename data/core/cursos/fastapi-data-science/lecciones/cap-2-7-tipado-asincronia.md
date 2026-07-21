### 2.7 Tipado Estático (Type Hints) y Concurrencia (async/await)

FastAPI se distingue de otros frameworks web de Python (como Flask o Django tradicional) por integrar de forma nativa las anotaciones de tipo (PEP 484) y la concurrencia asíncrona mediante **ASGI**.

---

### 1. Tipado Estático (Type Hints) y Pydantic

Aunque Python sigue siendo de tipado dinámico en tiempo de ejecución, los *Type Hints* permiten a editores de código, linters y a **Pydantic** validar los tipos de entrada/salida de las peticiones HTTP.

#### Sintaxis Moderna (Python 3.10+)

```python
from typing import Annotated

# Operador '|' para tipos opcionales o uniones (sustituye a Union y Optional)
def procesar_lote_sensores(
    telemetria: list[float],
    modelo_id: str | None = None
) -> dict[str, float | str]:
    promedio = sum(telemetria) / len(telemetria) if telemetria else 0.0
    return {
        "promedio": round(promedio, 2),
        "modelo": modelo_id or "default_v1"
    }

# Annotated para metadata
def validar_frecuencia(hz: Annotated[float, "Frecuencia en Hertz"]) -> bool:
    return 47.5 <= hz <= 52.5
```

---

### 2. Programación Asíncrona (`async` y `await`)

Las aplicaciones web tradicionales ejecutan peticiones I/O de manera bloqueante (esperando respuestas de la base de datos o APIs externas mientras el procesador queda inactivo).

FastAPI utiliza el servidor **ASGI** Uvicorn y el bucle de eventos (*Event Loop*) de Python para manejar miles de conexiones concurrentes en un único hilo.

```python
import asyncio
from fastapi import FastAPI

app = FastAPI()

async def consultar_base_datos_async(sensor_id: str) -> dict:
    await asyncio.sleep(0.1)  # No bloquea el hilo; cede el control al Event Loop
    return {"sensor_id": sensor_id, "status": "activo", "valor": 98.4}

@app.get("/sensores/{sensor_id}")
async def get_sensor_info(sensor_id: str):
    data = await consultar_base_datos_async(sensor_id)
    return {"status": "success", "data": data}
```

> **¿Cuándo usar `async def` vs `def`?**
> - **`async def`**: Para llamadas I/O no bloqueantes (ej. `httpx`, `asyncpg`, `aioredis`).
> - **`def`**: Para código bloqueante o CPU-bound pesado (ej. `scikit-learn`, `numpy`, `pandas`). FastAPI ejecutará automáticamente los endpoints `def` en un *ThreadPool* separado sin congelar el servidor web.

---

### 3. Generadores (`yield`) para Streaming y Control de Memoria

Cuando procesas grandes datasets de entrenamiento o archivos CSV de varios gigabytes, cargarlos completamente en RAM provoca desbordamientos. Los **generadores** producen valores individualmente a demanda:

```python
from typing import Generator

def stream_registros_csv(file_path: str) -> Generator[str, None, None]:
    with open(file_path, "r", encoding="utf-8") as f:
        for linea in f:
            yield linea.strip()

# Procesamiento eficiente sin sobrecargar la memoria RAM
for fila in stream_registros_csv("telemetria_gigante.csv"):
    # Procesar fila por fila
    pass
```

---

### Resumen del Capítulo 2
Al dominar los fundamentos de Python, la indentación estricta, los tipos nativos, las estructuras de datos, el flujo de control, la orientación a objetos con métodos mágicos y la asincronía con `async/await`, estás 100% preparado para encarar el desarrollo de APIs RESTful de nivel profesional en FastAPI.
