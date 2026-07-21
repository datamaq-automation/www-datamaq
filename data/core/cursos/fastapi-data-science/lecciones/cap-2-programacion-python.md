### Conceptos Avanzados de Python para APIs y Ciencia de Datos

FastAPI se apoya en características modernas de Python para ofrecer validación automática, autocompletado en el editor de código y documentación OpenAPI sin código repetitivo. En esta lección profundizaremos en los tres pilares de Python moderno necesarios para construir APIs de Machine Learning de alto rendimiento.

---

### 1. Tipado Estático (Type Hints)

El tipado en Python fue introducido formalmente en PEP 484. FastAPI utiliza estas anotaciones para realizar validación de datos en tiempo de ejecución (a través de Pydantic) y para generar la documentación OpenAPI interactiva.

#### Sintaxis Básica de Anotaciones

```python
# Tipado de variables y parámetros de función
def calcular_eficiencia_motor(potencia_kw: float, horas_uso: int) -> float:
    return potencia_kw * horas_uso * 0.85

# Tipado de colecciones (Python 3.9+)
sensores: list[str] = ["temperatura", "presion", "vibracion"]
lecturas: dict[str, float] = {"temperatura": 42.5, "presion": 1.013}
```

#### Módulo `typing` y Sintaxis Moderna (Python 3.10+)

```python
from typing import Optional, Union, Annotated

# En Python 3.10+ puedes usar la barra vertical '|' en lugar de Union / Optional
def obtener_prediccion_modelo(
    input_data: list[float],
    model_version: str | None = None
) -> dict[str, float | str]:
    # Lógica de inferencia
    return {"prediction": 0.94, "status": "ok"}

# Annotated permite adjuntar metadata adicional a las anotaciones de tipo
def validar_temperatura(val: Annotated[float, "Grados Celsius"]) -> bool:
    return -50.0 <= val <= 150.0
```

---

### 2. Programación Asíncrona (`async` y `await`)

Las aplicaciones tradicionales de Python operan de manera síncrona y bloqueante: cuando un hilo realiza una operación de I/O (lectura de base de datos, consulta a API externa o lectura de disco), el procesador queda inactivo esperando la respuesta.

FastAPI es un framework **ASGI** (Asynchronous Server Gateway Interface) capaz de manejar miles de conexiones concurrentes en un único hilo gracias al Event Loop de Python.

#### Conceptos Clave:
- **`async def`**: Define una función corrutina asíncrona.
- **`await`**: Pausa la ejecución de la corrutina actual y devuelve el control al Event Loop hasta que la tarea asíncrona finalice, permitiendo procesar otras peticiones entrantes.

#### Ejemplo de Endpoint Asíncrono en FastAPI

```python
import asyncio
from fastapi import FastAPI

app = FastAPI()

# Simulación de llamada I/O no bloqueante a una base de datos o servicio externo
async def consultar_base_datos_sensores(sensor_id: str) -> dict:
    await asyncio.sleep(0.5)  # No bloquea el hilo principal
    return {"sensor_id": sensor_id, "valor": 98.6}

@app.get("/sensores/{sensor_id}")
async def get_sensor_data(sensor_id: str):
    data = await consultar_base_datos_sensores(sensor_id)
    return {"status": "success", "data": data}
```

> **¿Cuándo usar `async def` vs `def`?**
> - Usa `async def` cuando utilices librerías asíncronas de I/O (ej. `httpx`, `asyncpg`, `motor`).
> - Usa `def` estándar cuando ejecutes tareas CPU-bound pesadas de Machine Learning (ej. inferencia pesada con `scikit-learn`, `numpy` o `torch`). FastAPI ejecutará automáticamente los endpoints `def` en un pool de hilos separado (threadpool) para no bloquear el Event Loop.

---

### 3. List Comprehensions, Dict Comprehensions y Generadores

En Ciencia de Datos es habitual procesar grandes flujos de métricas antes de retornarlos en las respuestas HTTP.

#### List Comprehensions y Dict Comprehensions

Permiten transformar e filtrar colecciones de datos con una sintaxis limpia y eficiente:

```python
mediciones_raw = [12.4, -999.0, 15.1, 14.8, -999.0, 16.3]

# Filtrar lecturas nulas (-999.0) y convertir a escala normalizada
mediciones_limpias = [val / 100.0 for val in mediciones_raw if val != -999.0]
# Resultado: [0.124, 0.151, 0.148, 0.163]

# Dict comprehension para mapear sensores a su estado
sensores_ids = ["s1", "s2", "s3"]
estados = ["ok", "alerta", "ok"]
mapa_sensores = {sid: estado for sid, estado in zip(sensores_ids, estados)}
```

#### Generadores (`yield`) para Procesamiento Eficiente de Memoria

Cuando se procesan grandes datasets o archivos CSV de entrenamiento de varios gigabytes, almacenar toda la estructura en memoria puede agotar la RAM del servidor. Los **generadores** producen elementos de uno en uno bajo demanda:

```python
from typing import Generator

def stream_lineas_dataset(file_path: str) -> Generator[str, None, None]:
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()

# Iteración eficiente sobre millones de registros sin cargarlos todos en la RAM
for linea in stream_lineas_dataset("datos_sensores_gigantes.csv"):
    # Procesar línea individualmente
    pass
```

---

### Resumen de la Lección

Comprender la interacción entre **Type Hints**, **async/await** y las **estructuras eficientes de Python** es el paso indispensable antes de escribir endpoints de producción en FastAPI. En el siguiente capítulo construiremos nuestra primera API RESTful desde cero.
