### 3.1 Desarrollo de una API RESTful con FastAPI

En esta lección práctica construiremos nuestra primera API RESTful desde cero utilizando FastAPI y el servidor ASGI Uvicorn. Aprenderemos la estructura básica de una aplicación web, la definición de rutas HTTP, la gestión de parámetros de consulta y la documentación interactiva OpenAPI.

---

### 1. Estructura Inicial de la Aplicación (`main.py`)

Crea un archivo llamado `main.py` en la raíz de tu proyecto e ingresa el siguiente código:

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

# Inicialización de la instancia principal de la aplicación
app = FastAPI(
    title="API de Diagnóstico Industrial y Ciencia de Datos",
    description="API RESTful para inferencia de modelos de ML y monitoreo de sensores",
    version="1.0.0"
)

# Base de datos simulada en memoria
base_datos_equipos = {
    1: {"nombre": "Bomba Centrifuga A1", "vibracion": 0.04, "estado": "optimo"},
    2: {"nombre": "Compresor de Aire C3", "vibracion": 0.18, "estado": "advertencia"},
}

@app.get("/", tags=["General"])
def read_root():
    return {
        "mensaje": "Bienvenido a la API de Ciencia de Datos DataMaq",
        "status": "online",
        "version": "1.0.0"
    }
```

---

### 2. Parámetros de Ruta (Path Parameters) y Manejo de Errores

Los **parámetros de ruta** permiten capturar valores variables dentro de la URL. FastAPI valida automáticamente que el parámetro coincida con el tipo de dato especificado en las anotaciones de Python:

```python
@app.get("/equipos/{equipo_id}", tags=["Equipos"])
def obtener_equipo(equipo_id: int):
    """
    Obtiene los detalles y lecturas de un equipo industrial por su ID único.
    """
    if equipo_id not in base_datos_equipos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipo con ID {equipo_id} no fue encontrado en el sistema."
        )
    return base_datos_equipos[equipo_id]
```

---

### 3. Parámetros de Consulta (Query Parameters) con Valores por Defecto

Los parámetros de la función que no forman parte de la ruta en la URL son interpretados automáticamente como **parámetros de consulta** (Query Parameters, ej: `/equipos?estado=optimo&limit=10`):

```python
@app.get("/equipos", tags=["Equipos"])
def listar_equipos(estado: str | None = None, limite: int = 10):
    """
    Lista los equipos filtrados opcionalmente por estado.
    """
    resultado = list(base_datos_equipos.values())
    
    if estado:
        resultado = [eq for eq in resultado if eq["estado"] == estado]
        
    return resultado[:limite]
```

---

### 4. Creación de Recursos con Métodos POST

Para recibir datos complejos en el cuerpo de la petición (Request Body), definiremos una estructura tipada usando Pydantic:

```python
class NuevoEquipo(BaseModel):
    nombre: str
    vibracion: float
    estado: str = "optimo"

@app.post("/equipos", status_code=status.HTTP_201_CREATED, tags=["Equipos"])
def crear_equipo(equipo: NuevoEquipo):
    nuevo_id = max(base_datos_equipos.keys(), default=0) + 1
    base_datos_equipos[nuevo_id] = equipo.model_dump()
    return {"id": nuevo_id, "equipo": base_datos_equipos[nuevo_id]}
```

---

### 5. Ejecución del Servidor con Uvicorn

Para poner en marcha la API con recarga automática en tiempo real ante cualquier cambio en el código (live reload), ejecuta en la terminal:

```bash
uvicorn main:app --reload --port 8000
```

Explicación del comando:
- `main`: nombre del archivo Python (`main.py`).
- `app`: nombre de la variable de la instancia de `FastAPI()`.
- `--reload`: habilita el reinicio automático del servidor al guardar modificaciones en los archivos.

---

### 6. Pruebas de la API con HTTPie y Documentación OpenAPI

Una vez que el servidor esté corriendo en `http://127.0.0.1:8000`:

#### Probar endpoints en la terminal con HTTPie:

```bash
# Probar la raíz
http GET http://127.0.0.1:8000/

# Obtener un equipo existente
http GET http://127.0.0.1:8000/equipos/1

# Probar error 404
http GET http://127.0.0.1:8000/equipos/999

# Crear un nuevo equipo mediante POST
http POST http://127.0.0.1:8000/equipos nombre="Torno CNC X" vibracion:=0.02 estado="optimo"
```

#### Documentación Interactiva de la API:

FastAPI genera automáticamente documentación interactiva accesible desde tu navegador:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) - Permite probar todos los endpoints interactivamente sin cliente HTTP externo.
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) - Formato de documentación estructurado para equipos de desarrollo.
