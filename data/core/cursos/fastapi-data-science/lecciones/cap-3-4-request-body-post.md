### 3.4 Cuerpo de la Petición y Múltiples Objetos (The Request Body & Multiple Objects)

En APIs de producciones web y Machine Learning, el cliente necesita enviar payloads complejos estructurados en JSON dentro del **Cuerpo de la Petición** (*Request Body*). FastAPI utiliza **Pydantic** para deserializar, validar y combinar múltiples objetos y tipos en el payload.

---

### 1. El Cuerpo de la Petición (The Request Body)

Para declarar que un endpoint espera un payload JSON en el cuerpo de la petición HTTP, creamos una subclase de `pydantic.BaseModel` y la anotamos como argumento en el controlador:

```python
from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI(title="API Request Body Single Model")

class LecturaSensor(BaseModel):
    sensor_id: str = Field(..., description="ID del sensor")
    temperatura: float = Field(..., ge=-50.0, le=150.0)
    presion: float = Field(..., gt=0.0)
    activo: bool = True

@app.post("/sensor/lectura", status_code=status.HTTP_201_CREATED)
def registrar_lectura(lectura: LecturaSensor):
    """
    JSON esperado en el Body:
    {
        "sensor_id": "s1",
        "temperatura": 42.5,
        "presion": 10.2,
        "activo": true
    }
    """
    return {"status": "registrado", "datos": lectura.model_dump()}
```

---

### 2. Múltiples Objetos en el Request Body (Multiple Body Objects)

Cuando un endpoint necesita recibir **dos o más modelos de Pydantic independientes** en la misma petición, FastAPI los combina automáticamente esperando un objeto JSON de primer nivel cuyas claves coincidan con los nombres de los argumentos:

```python
from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

class DatosEquipo(BaseModel):
    nombre: str
    fabricante: str

class ConfiguracionRed(BaseModel):
    ip_address: str
    puerto: int

@app.post("/equipo/configurar")
def configurar_equipo_completo(
    equipo: DatosEquipo,              # Objeto 1
    red: ConfiguracionRed,            # Objeto 2
    prioridad: int = Body(..., ge=1, le=5) # Valor escalar en el Body con Body()
):
    """
    JSON esperado en el Body con MÚLTIPLES objetos y un escalar:
    {
        "equipo": {
            "nombre": "Torno CNC A",
            "fabricante": "Siemens"
        },
        "red": {
            "ip_address": "192.168.1.100",
            "puerto": 502
        },
        "prioridad": 3
    }
    """
    return {
        "equipo": equipo,
        "red": red,
        "prioridad": prioridad,
        "status": "configurado"
    }
```

---

### 3. Envolver un Único Modelo con `Body(embed=True)`

Por defecto, cuando declaras un único modelo de Pydantic, FastAPI espera que el JSON recibido sea directamente el objeto (ej. `{"nombre": "Torno"}`). Si deseas que el JSON esté envuelto bajo una clave principal con el nombre del parámetro (ej. `{"item": {"nombre": "Torno"}}`), utiliza `Body(embed=True)`:

```python
@app.post("/equipo/embebido")
def crear_equipo_embebido(
    equipo: DatosEquipo = Body(..., embed=True)
):
    """
    JSON esperado en el Body:
    {
        "equipo": {
            "nombre": "Prensa Hidráulica",
            "fabricante": "Bosch"
        }
    }
    """
    return equipo
```

---

### 4. Modelos Anidados y Listas de Objetos (Nested Models & Lists)

#### A. Modelos Anidados (Nested Models)
Los atributos de un modelo Pydantic pueden ser otros modelos Pydantic, permitiendo definir estructuras jerárquicas complejas:

```python
class Componente(BaseModel):
    nombre: str
    serie: str

class MaquinaCompleja(BaseModel):
    maquina_id: str
    componentes: list[Componente]  # Lista de modelos anidados

@app.post("/maquina/ensamblar")
def registrar_maquina(maquina: MaquinaCompleja):
    """
    JSON esperado:
    {
        "maquina_id": "MQ-900",
        "componentes": [
            {"nombre": "Motor", "serie": "MOT-12"},
            {"nombre": "Rodamiento", "serie": "ROD-88"}
        ]
    }
    """
    return {"maquina": maquina.maquina_id, "total_componentes": len(maquina.componentes)}
```

#### B. Lista de Objetos en la Raíz del Body (`list[Model]`)
Si tu endpoint recibe directamente un arreglo JSON de objetos en la raíz del body:

```python
@app.post("/sensores/lote")
def procesar_lote_sensores(lecturas: list[LecturaSensor]):
    """
    JSON esperado (Array en la raíz):
    [
        {"sensor_id": "s1", "temperatura": 20.0, "presion": 1.0},
        {"sensor_id": "s2", "temperatura": 25.5, "presion": 1.2}
    ]
    """
    return {
        "lote_procesado": len(lecturas),
        "sensores_ids": [s.sensor_id for s in lecturas]
    }
```

---

### Resumen de la Lección
FastAPI brinda flexibilidad total para procesar el *Request Body*: desde un único modelo Pydantic, pasando por la combinación de **múltiples objetos** y escalares con `Body()`, hasta modelos anidados y listas completas en la raíz del JSON.
