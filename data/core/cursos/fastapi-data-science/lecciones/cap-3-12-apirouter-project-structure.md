### 3.12 Respuestas Personalizadas y Estructuración de Proyectos con APIRouter

A medida que una aplicación web o plataforma de Ciencia de Datos crece, mantener todas las rutas en un único archivo `main.py` se vuelve inmanejable. FastAPI provee la clase **`APIRouter`** para modularizar las rutas en múltiples archivos independientes y administrar clases de respuesta personalizadas (*Custom Responses*).

---

### 1. Respuestas Personalizadas Avanzadas (Custom Responses)

FastAPI permite definir la clase de respuesta por defecto a nivel de aplicación o de enrutador mediante el argumento `default_response_class`.

```python
from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse, ORJSONResponse

# Configura HTMLResponse como la respuesta predeterminada para esta app/router
app = FastAPI(default_response_class=ORJSONResponse)

@app.get("/custom-orjson")
def get_fast_json():
    # ORJSONResponse serializa datetimes, numpy arrays y dataclasses a alta velocidad
    return {"status": "ok", "procesado": True}
```

---

### 2. Estructuración de Proyectos Complejos con `APIRouter`

En proyectos de producción, la arquitectura recomendada organiza el código por capas y subdominios funcionales:

```text
mi_proyecto_fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Punto de entrada e instanciación de FastAPI
│   ├── core/                    # Configuración global y seguridad
│   │   ├── __init__.py
│   │   └── config.py
│   ├── routers/                 # Routers modulares por entidad o módulo
│   │   ├── __init__.py
│   │   ├── sensores.py
│   │   ├── modelos_ml.py
│   │   └── usuarios.py
│   └── schemas/                 # Modelos de Pydantic
│       ├── __init__.py
│       └── sensor_schema.py
```

---

### 3. Creación de Routers Modulares (`APIRouter`)

Cada archivo en `app/routers/` declara su propio objeto `APIRouter`, aislando los endpoints de su dominio.

#### Ejemplo 1: `app/routers/sensores.py`
```python
from fastapi import APIRouter, status, HTTPException

router = APIRouter(
    prefix="/sensores",
    tags=["Monitoreo de Sensores"],
    responses={404: {"description": "Sensor no encontrado"}}
)

sensores_db = {"s1": {"temp": 42.5}, "s2": {"temp": 88.0}}

@router.get("/")
def listar_sensores():
    return list(sensores_db.values())

@router.get("/{sensor_id}")
def obtener_sensor(sensor_id: str):
    if sensor_id not in sensores_db:
        raise HTTPException(status_code=404, detail="Sensor no registrado")
    return sensores_db[sensor_id]
```

#### Ejemplo 2: `app/routers/modelos_ml.py`
```python
from fastapi import APIRouter, status

router = APIRouter(
    prefix="/modelos",
    tags=["Inferencia Machine Learning"]
)

@router.post("/predict", status_code=status.HTTP_200_OK)
def predecir_anomalia(features: list[float]):
    return {"prediccion": "Normal", "confianza": 0.98}
```

---

### 4. Montaje de Routers en la Aplicación Principal (`app/main.py`)

En el archivo de entrada `main.py`, importamos los routers individuales e integramos sus rutas utilizando **`app.include_router()`**:

```python
from fastapi import FastAPI
from app.routers import sensores, modelos_ml

app = FastAPI(
    title="Plataforma de Ciencia de Datos DataMaq",
    description="API Modular para Telemetría y Modelos de ML",
    version="2.0.0"
)

# Incluir los routers modulares bajo el prefijo global /api/v1
app.include_router(sensores.router, prefix="/api/v1")
app.include_router(modelos_ml.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"mensaje": "API Modular DataMaq v2.0 Online"}
```

#### Resultado de URLs Generadas:
- `GET /api/v1/sensores/` $\rightarrow$ Lista todos los sensores.
- `GET /api/v1/sensores/{sensor_id}` $\rightarrow$ Detalle de sensor.
- `POST /api/v1/modelos/predict` $\rightarrow$ Inferencia de ML.

---

### Resumen de la Lección
Usar `APIRouter` permite desacoplar los endpoints por dominios funcionales, reutilizar prefijos (`/api/v1/sensores`), etiquetas para Swagger UI y dependencias comunes, logrando una arquitectura de código limpia, mantenible y escalable a grandes equipos de desarrollo.
