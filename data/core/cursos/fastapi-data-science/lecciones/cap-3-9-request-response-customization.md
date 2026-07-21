### 3.9 Objeto Request, Respuestas Personalizadas y Configuración de Operaciones

FastAPI proporciona acceso de bajo nivel a las peticiones HTTP entrantes mediante el objeto **`Request`**, control total sobre las respuestas enviadas mediante el parámetro **`Response`** y clases de respuesta personalizadas, así como una amplia suite de **parámetros de operación de ruta** (*Path Operation Parameters*) para enriquecer la documentación OpenAPI.

---

### 1. El Objeto `Request` (The Request Object)

En ocasiones se requiere acceder directamente a los metadatos crudos de la petición HTTP recibida (como la dirección IP del cliente, las cabeceras HTTP crudas o la URL completa). Podemos inyectar el objeto **`Request`** importado desde `fastapi`:

```python
from fastapi import FastAPI, Request

app = FastAPI(title="API Request Object")

@app.get("/auditoria/cliente")
async def auditar_cliente(request: Request):
    """
    Accede directamente a los datos crudos del objeto Request de Starlette/FastAPI.
    """
    ip_cliente = request.client.host if request.client else "Desconocido"
    puerto_cliente = request.client.port if request.client else 0
    url_completa = str(request.url)
    metodo = request.method
    headers = dict(request.headers)
    
    # Leer el cuerpo crudo de la petición
    body_bytes = await request.body()
    
    return {
        "metodo": metodo,
        "url": url_completa,
        "ip_origen": ip_cliente,
        "puerto_origen": puerto_cliente,
        "user_agent": headers.get("user-agent"),
        "tamano_body_bytes": len(body_bytes)
    }
```

---

### 2. El Parámetro `Response`: Headers y Código de Estado Dinámico

Inyectar el parámetro **`response: Response`** permite modificar el código de estado HTTP o añadir cabeceras personalizadas dinámicamente según la lógica en tiempo de ejecución, sin necesidad de instanciar o retornar manualmente un objeto `Response`.

#### A. Establecer Encabezados (Setting Headers)
```python
response.headers["X-Custom-Header"] = "DataMaq-v1"
```

#### B. Cambiar el Código de Estado Dinámicamente (Setting the Status Code Dynamically)

```python
from fastapi import FastAPI, Response, status

app = FastAPI()

# Base de datos simulada de tareas en segundo plano
tareas_procesadas = {"t1": "completado"}

@app.post("/tareas/{tarea_id}/procesar")
def procesar_tarea_dinamica(tarea_id: str, response: Response):
    """
    Cambia dinámicamente el código de estado HTTP:
    - 200 OK si ya fue procesada anteriormente.
    - 202 Accepted si se envió a procesar en segundo plano.
    """
    response.headers["X-Processing-Node"] = "Worker-01"

    if tarea_id in tareas_procesadas:
        # Tarea ya terminada -> 200 OK
        response.status_code = status.HTTP_200_OK
        return {"tarea_id": tarea_id, "estado": tareas_procesadas[tarea_id]}
    else:
        # Tarea enviada a segundo plano -> 202 Accepted
        tareas_procesadas[tarea_id] = "en_proceso"
        response.status_code = status.HTTP_202_ACCEPTED
        return {"tarea_id": tarea_id, "mensaje": "Tarea aceptada para procesamiento asíncrono"}
```

---

### 3. Personalización de Respuestas (Customizing the Response)

FastAPI permite retornar directamente distintas clases de respuesta importadas desde `fastapi.responses`:

| Clase de Respuesta | Uso Principal | Content-Type |
| :--- | :--- | :--- |
| **`JSONResponse`** | Respuestas JSON estructuradas manuales | `application/json` |
| **`HTMLResponse`** | Renderizado de código HTML directamente | `text/html` |
| **`PlainTextResponse`** | Texto plano o archivos de configuración | `text/plain` |
| **`RedirectResponse`** | Redirecciones HTTP (código 302, 301, 307) | N/A |
| **`StreamingResponse`** | Transmisión continua en tiempo real de streams o video | Configurable |
| **`FileResponse`** | Descarga asíncrona de archivos binarios | Configurable |

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse

app = FastAPI()

@app.get("/landing", response_class=HTMLResponse)
def get_html_landing():
    return """
    <html>
        <head><title>DataMaq Monitoreo</title></head>
        <body><h1>Panel de Control Industrial</h1></body>
    </html>
    """

@app.get("/logs/raw", response_class=PlainTextResponse)
def get_log_plano():
    return "INFO 2026-07-21 - Operación sin anomalías\nWARN 2026-07-21 - Alta temperatura"

@app.get("/legacy-url")
def redireccionar_v2():
    return RedirectResponse(url="/landing", status_code=307)
```

---

### 4. Parámetros de Operación de Ruta (Path Operation Parameters)

Podemos enriquecer la documentación interactiva OpenAPI configurando los metadatos del decorador `@app.get()` / `@app.post()`:

```python
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class SensorOut(BaseModel):
    id: str
    valor: float

@app.get(
    "/sensores/criticos",
    response_model=list[SensorOut],
    status_code=status.HTTP_200_OK,
    tags=["Monitoreo Industrial"],
    summary="Obtiene la lista de sensores con lecturas críticas",
    description="""
    Filtra en la base de datos distribuida los sensores cuyo valor supere el umbral.
    - **Retorna**: Lista de objetos `SensorOut`.
    - **Cache**: Revalida cada 5 segundos.
    """,
    response_description="Lista filtrada de sensores en estado de alerta",
    deprecated=False,
    responses={
        404: {"description": "No se encontraron sensores registrados"},
        503: {"description": "Servicio de base de datos no disponible"}
    }
)
def listar_sensores_criticos():
    return [{"id": "s1", "valor": 98.4}]
```

#### Atributos Configurados:
- `summary`: Título corto que aparece junto al endpoint en Swagger UI.
- `description`: Descripción larga en formato Markdown.
- `response_description`: Descripción del objeto devuelto.
- `tags`: Clasificación jerárquica en bloques dentro de la documentación.
- `responses`: Diccionario con esquemas de códigos de error adicionales (`404`, `503`).

---

### Resumen de la Lección
El objeto `Request` brinda acceso de bajo nivel a los datos crudos de la llamada, el parámetro `Response` permite ajustar dinámicamente códigos de estado (como `202 Accepted`) y encabezados, las respuestas personalizadas (`HTMLResponse`, `PlainTextResponse`, `RedirectResponse`) extienden los formatos soportados y los *Path Operation Parameters* transforman la documentación OpenAPI en una referencia profesional.
