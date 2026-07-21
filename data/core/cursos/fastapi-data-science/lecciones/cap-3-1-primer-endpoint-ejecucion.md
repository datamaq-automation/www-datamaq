### 3.1 Creación del Primer Endpoint y Ejecución Local (Creating the First Endpoint)

En esta lección aprenderás a crear tu primera aplicación FastAPI, definir un endpoint básico utilizando decoradores de operaciones HTTP y poner a funcionar el servidor de desarrollo local mediante **Uvicorn**.

---

### 1. Estructura de la Aplicación en FastAPI

FastAPI utiliza decoradores de Python (como `@app.get()`, `@app.post()`) para vincular una ruta URL y un método HTTP específico a una función controladora (*path operation function*).

#### Creación del archivo `chapter3_first_endpoint.py`:

```python
from fastapi import FastAPI

# 1. Crear la instancia principal de la aplicación FastAPI
app = FastAPI(
    title="DataMaq API - Primer Endpoint",
    description="API inicial de diagnóstico para telemetría industrial",
    version="1.0.0"
)

# 2. Definir una operación de ruta GET en la raíz "/"
@app.get("/")
def read_root():
    """
    Endpoint de bienvenida que confirma el estado operativo de la API.
    """
    return {
        "mensaje": "¡Bienvenido a la API de Ciencia de Datos y Telemetría DataMaq!",
        "estado": "online",
        "version": "1.0.0"
    }

# 3. Endpoint secundario de estado de salud (Healthcheck)
@app.get("/health", tags=["Monitoreo"])
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "cpu_usage_percent": 12.4
    }
```

---

### 2. Ejecución Local con Uvicorn (Running Locally)

**Uvicorn** es un servidor web **ASGI** (Asynchronous Server Gateway Interface) ultrarrápido escrito en Python sobre `uvloop` y `httptools`.

Para iniciar el servidor local en la terminal, ejecuta:

```bash
uvicorn chapter3_first_endpoint:app --reload --port 8000
```

#### Desglose de Argumentos del Comando:
- `chapter3_first_endpoint`: Nombre del módulo o archivo Python (sin la extensión `.py`).
- `:app`: Nombre de la variable dentro del script que contiene la instancia `FastAPI()`.
- `--reload`: Habilita la recarga automática (*live reload*). El servidor se reiniciará automáticamente ante cualquier guardado de código.
- `--port 8000`: Especifica el puerto TCP en el cual escuchará peticiones (por defecto `8000`).

#### Salida en la Terminal:
```text
INFO:     Will watch for changes in these directories: ['/home/agustin/proyectos_software/www-datamaq']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [18452] using StatReload
INFO:     Started server process [18454]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

### 3. Verificación del Endpoint

Una vez iniciado el servidor en `http://127.0.0.1:8000`, puedes probar la respuesta mediante cualquier navegador o desde la terminal con `curl` o `HTTPie`.

#### Prueba desde la consola con `curl`:
```bash
curl -X GET "http://127.0.0.1:8000/"
```

#### Respuesta JSON recibida:
```json
{
  "mensaje": "¡Bienvenido a la API de Ciencia de Datos y Telemetría DataMaq!",
  "estado": "online",
  "version": "1.0.0"
}
```

---

### Resumen de la Lección
Has creado tu primera API web en FastAPI y la has ejecutado localmente con Uvicorn. En la siguiente lección aprenderemos a capturar parámetros dinámicos en la URL (*Path Parameters*).
