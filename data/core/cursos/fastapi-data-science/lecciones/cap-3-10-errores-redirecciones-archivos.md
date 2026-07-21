### 3.10 Excepciones HTTP, Respuestas Personalizadas, Redirecciones y Archivos (HTTP Errors & Custom Responses)

En esta lección abordaremos cómo manejar excepciones de negocio elevando errores HTTP, construir respuestas personalizadas crudas, efectuar redirecciones entre rutas y servir archivos binarios para descarga mediante **`FileResponse`**.

---

### 1. Elevando Errores HTTP (Raising HTTP Errors)

Cuando ocurre un fallo de validación o un recurso no existe, elevamos una excepción de tipo **`HTTPException`**. FastAPI captura esta excepción y la convierte automáticamente en una respuesta JSON estructurada con el código de estado indicado.

#### A. Uso de `HTTPException` con Detalle y Headers
```python
from fastapi import FastAPI, HTTPException, status

app = FastAPI(title="API de Errores HTTP")

base_datos_modelos = {"v1": "XGBoost_v1.pkl"}

@app.get("/modelos/descargar/{modelo_id}")
def obtener_modelo_weights(modelo_id: str):
    if modelo_id not in base_datos_modelos:
        # Eleva error 404 Not Found con metadatos y encabezados de error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "MODEL_NOT_FOUND",
                "mensaje": f"El modelo '{modelo_id}' no está registrado en el repositorio.",
                "modelos_disponibles": list(base_datos_modelos.keys())
            },
            headers={"X-Error-Category": "MachineLearningModel"}
        )
    return {"modelo_id": modelo_id, "file": base_datos_modelos[modelo_id]}
```

#### B. Manejadores de Excepciones Personalizados (Custom Exception Handlers)
Podemos capturar excepciones personalizadas de Python y formatear la respuesta globalmente:

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class SensorOfflineException(Exception):
    def __init__(self, sensor_id: str):
        self.sensor_id = sensor_id

@app.exception_handler(SensorOfflineException)
def sensor_offline_handler(request: Request, exc: SensorOfflineException):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "status": "error",
            "categoria": "HARDWARE_OFFLINE",
            "detail": f"El sensor industrial '{exc.sensor_id}' está fuera de línea."
        }
    )
```

---

### 2. Construcción de Respuestas Personalizadas (Building a Custom Response)

Si necesitás retornar una estructura JSON cruda sin pasar por los convertidores de Pydantic, o devolver respuestas con formatos no estándar, podés instanciar directamente **`JSONResponse`**, **`HTMLResponse`** o **`PlainTextResponse`**:

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse

app = FastAPI()

@app.get("/custom/json")
def get_custom_json():
    # Instanciación explícita de JSONResponse con status y headers
    return JSONResponse(
        status_code=202,
        content={"mensaje": "Solicitud aceptada en cola de procesamiento"},
        headers={"X-Queue-Position": "12"}
    )

@app.get("/custom/html", response_class=HTMLResponse)
def get_custom_html():
    return HTMLResponse(
        content="<h1>DataMaq Telemetría</h1><p>Estado del sistema: OK</p>",
        status_code=200
    )
```

---

### 3. Efectuar Redirecciones (Making a Redirection)

Para redirigir al cliente hacia otra URL o endpoint (por ejemplo, cuando una versión previa de la API ha quedado obsoleta), se utiliza **`RedirectResponse`**:

- **`307 Temporary Redirect`** (Recomendado en FastAPI): Mantiene el método HTTP original (`GET`, `POST`) en la nueva URL.
- **`301 Moved Permanently`**: Redirección permanente que los navegadores almacenan en caché.

```python
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/v1/sensores")
def listar_sensores_legacy():
    """
    Redirige peticiones de la API v1 obsoleta hacia la API v2.
    """
    return RedirectResponse(
        url="/v2/sensores",
        status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )

@app.get("/v2/sensores")
def listar_sensores_v2():
    return [{"id": "s1_v2", "version": "2.0.0"}]
```

---

### 4. Servir Archivos para Descarga (Serving a File)

Para enviar archivos binarios desde el disco del servidor hacia el cliente (archivos CSV, reportes PDF o imágenes), se utiliza **`FileResponse`**:

```python
import os
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse, StreamingResponse

app = FastAPI()

@app.get("/reportes/descargar-csv")
def descargar_reporte_csv():
    file_path = "data/export/reporte_telemetria.csv"
    
    # 1. Verificar existencia del archivo
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El archivo de reporte no existe en el servidor."
        )
        
    # 2. Retornar el archivo forzando su descarga en el navegador (media_type y filename)
    return FileResponse(
        path=file_path,
        filename="reporte_telemetria_2026.csv",  # Nombre sugerido al descargar
        media_type="text/csv"
    )
```

#### Transmisión Continua con `StreamingResponse`:
Para transmitir grandes volúmenes de datos en tiempo real (ej. streams de audio/video o generación de CSV al vuelo):

```python
def generar_lineas_csv():
    yield "sensor_id,temperatura,timestamp\n"
    for i in range(1, 100):
        yield f"s_{i},22.5,2026-07-21\n"

@app.get("/stream/csv")
def stream_csv():
    return StreamingResponse(
        generar_lineas_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=stream_datos.csv"}
    )
```

---

### Resumen de la Lección
Elevar excepciones con `HTTPException`, construir respuestas personalizadas con `JSONResponse`, realizar redirecciones limpias con `RedirectResponse` y servir descargas de archivos con `FileResponse` completan el conjunto de herramientas esenciales para controlar las entradas y salidas de una API profesional en FastAPI.
