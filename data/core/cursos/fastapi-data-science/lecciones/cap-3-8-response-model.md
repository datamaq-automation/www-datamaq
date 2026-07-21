### 3.8 Modelos de Respuesta y Filtros de Salida (The Response Model)

En FastAPI, el parámetro **`response_model`** declarado en los decoradores de operación de ruta determina cómo se filtran, validan, documentan y convierten los datos que el endpoint retorna hacia el cliente.

---

### 1. ¿Por qué usar `response_model`?

Al declarar un `response_model`:
1. **Seguridad y Filtrado de Datos**: Garantiza que campos sensibles o privados (como contraseñas, hashes o campos internos de la base de datos) nunca sean expuestos en la respuesta JSON.
2. **Conversión y Validación de Salida**: Formatea y convierte automáticamente objetos ORM, diccionarios o modelos internos al esquema de salida esperado.
3. **Documentación OpenAPI**: Genera automáticamente los esquemas JSON de respuesta en Swagger UI (`/docs`).

```python
from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr

app = FastAPI(title="API Response Model")

# Schema de entrada (incluye la contraseña en texto plano)
class UsuarioInput(BaseModel):
    username: str
    email: EmailStr
    password: str

# Schema de salida (excluye la contraseña por seguridad)
class UsuarioOutput(BaseModel):
    id: int
    username: str
    email: EmailStr
    activo: bool = True

# Base de datos simulada
usuarios_db = {}

@app.post(
    "/usuarios",
    response_model=UsuarioOutput,  # Define el schema estricto de salida
    status_code=status.HTTP_201_CREATED
)
def registrar_usuario(usuario: UsuarioInput):
    nuevo_id = len(usuarios_db) + 1
    # En producción se guardarían el hash de la contraseña y metadatos internos
    registro_interno = {
        "id": nuevo_id,
        "username": usuario.username,
        "email": usuario.email,
        "hashed_password": f"hash_seguro_{usuario.password}",
        "activo": True,
        "internal_note": "Registrado desde API"
    }
    usuarios_db[nuevo_id] = registro_interno
    
    # Retornamos el diccionario completo, pero FastAPI filtrará SOLO los campos de UsuarioOutput
    return registro_interno
```

*Respuesta JSON filtrada recibida por el cliente:*
```json
{
  "id": 1,
  "username": "agustin",
  "email": "agustin@datamaq.com",
  "activo": true
}
```
*(Se omiten automáticamente `hashed_password` e `internal_note`)*

---

### 2. Filtrado de Valores Opcionales y Nulos

FastAPI ofrece argumentos en el decorador para personalizar cómo se comportan los valores devueltos:

#### A. `response_model_exclude_unset=True`
Omite en la respuesta JSON aquellos campos del modelo que no fueron asignados explícitamente al instanciarlo (dejando fuera los valores por defecto no utilizados):

```python
class MetricaOutput(BaseModel):
    sensor_id: str
    temperatura: float
    presion: float = 1.0
    vibracion: float = 0.0

@app.get("/metrica/unset", response_model=MetricaOutput, response_model_exclude_unset=True)
def obtener_metrica_sin_unset():
    # Si solo instanciamos sensor_id y temperatura, los valores por defecto sin asignar no se enviarán
    return MetricaOutput(sensor_id="s1", temperatura=42.5)
```

#### B. `response_model_exclude_none=True`
Omite cualquier campo cuyo valor sea `None`:

```python
@app.get("/metrica/sin-nulos", response_model=MetricaOutput, response_model_exclude_none=True)
def obtener_metrica_sin_nulos():
    return {"sensor_id": "s2", "temperatura": 36.6, "vibracion": None}
```

#### C. `response_model_include` y `response_model_exclude`
Permite incluir o excluir explícitamente una lista o conjunto de campos:

```python
@app.get(
    "/metrica/resumida",
    response_model=MetricaOutput,
    response_model_include={"sensor_id", "temperatura"}  # Solo envía estos dos campos
)
def obtener_metrica_resumida():
    return {"sensor_id": "s3", "temperatura": 99.1, "presion": 2.5, "vibracion": 0.1}
```

---

### 3. Respuestas de Listas y Colecciones (`list[Model]`)

Para retornar colecciones o arreglos JSON de modelos:

```python
@app.get("/usuarios", response_model=list[UsuarioOutput])
def listar_todos_los_usuarios():
    return list(usuarios_db.values())
```

---

### Resumen de la Lección
El parámetro `response_model` es la piedra angular de la seguridad en las respuestas de FastAPI. Garantiza que la API devuelva únicamente los datos autorizados, formateando listas y modelos de Pydantic con filtrado automático de campos privados.
