### 3.7 Encabezados HTTP y Cookies (Headers & Setting Cookies)

Los **encabezados HTTP** (*Headers*) y las **cookies** son fundamentales para gestionar autenticación, tokens de sesión, preferencias de usuario y metadatos de seguridad. FastAPI permite leer encabezados y cookies de la petición, así como configurar cookies seguras de respuesta mediante `response.set_cookie()`.

---

### 1. Encabezados HTTP de Petición (`Header`)

Para recibir encabezados enviados por el cliente (como `User-Agent`, `Authorization` o cabeceras personalizadas `X-Token`), utilizamos la función **`Header()`** de FastAPI.

#### Conversión Automática de Guiones
En HTTP las cabeceras suelen usar guiones (ejemplo: `User-Agent` o `X-Token`), mientras que en Python los guiones no son válidos en nombres de variables. FastAPI convierte automáticamente los guiones bajos `_` a guiones `-`:
- `user_agent: str = Header(...)` $\rightarrow$ Lee la cabecera `User-Agent`.
- `x_token: str = Header(...)` $\rightarrow$ Lee la cabecera `X-Token`.

```python
from fastapi import FastAPI, Header, status

app = FastAPI(title="API de Headers y Cookies")

@app.get("/telemetria/segura")
def obtener_telemetria_protegida(
    user_agent: str | None = Header(default=None),
    x_token: str = Header(..., description="Token de autorización en la cabecera X-Token")
):
    if x_token != "super-secret-token-123":
        return {"error": "Token de encabezado X-Token no válido"}
        
    return {
        "status": "acceso_concedido",
        "cliente_agent": user_agent,
        "token_validado": x_token
    }
```

---

### 2. Lectura de Cookies de Petición (`Cookie`)

Para acceder a las cookies almacenadas en el navegador o enviadas por el cliente HTTP en la cabecera `Cookie`, utilizamos la función **`Cookie()`**:

```python
from fastapi import FastAPI, Cookie

app = FastAPI()

@app.get("/usuario/perfil")
def obtener_perfil_usuario(
    session_id: str | None = Cookie(default=None, description="Cookie de sesión del cliente"),
    tema_preferido: str = Cookie(default="oscuro")
):
    if not session_id:
        return {"mensaje": "Usuario no autenticado (falta cookie session_id)"}
        
    return {
        "session_id": session_id,
        "tema": tema_preferido,
        "status": "autenticado"
    }
```

---

### 3. Configuración de Cookies de Respuesta (Setting Cookies)

Para enviar o guardar una cookie en el navegador del cliente desde un endpoint, inyectamos el objeto **`Response`** de FastAPI o retornamos una instancia de `JSONResponse` invocando el método **`response.set_cookie()`**.

#### Parámetros Principales de `set_cookie()`:

| Parámetro | Descripción | Recomendación de Seguridad |
| :--- | :--- | :--- |
| **`key`** | Nombre de la cookie | `session_token` |
| **`value`** | Contenido/token de la cookie | Cadena o JWT encriptado |
| **`max_age`** | Tiempo de vida en segundos | Ej. `3600` (1 hora) |
| **`httponly`** | Si es `True`, impide el acceso mediante JavaScript (`document.cookie`) | **`True`** (Mitiga ataques XSS) |
| **`secure`** | Si es `True`, solo se transmite a través de conexiones HTTPS cifradas | **`True`** en Producción |
| **`samesite`** | Controla el envío cross-site (`"lax"`, `"strict"`, `"none"`) | **`"lax"`** o **`"strict"`** (Protección CSRF) |
| **`domain` / `path`** | Restringe el dominio y la ruta URL donde la cookie es válida | Ej. `path="/"` |

#### Ejemplo Práctico: Login de Producción con Cookie Segura

```python
from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/auth/login", status_code=status.HTTP_200_OK)
def login_autenticar(response: Response, username: str, secret_key: str):
    """
    Establece una cookie de sesión HTTP-only segura en la respuesta.
    """
    if username != "operador" or secret_key != "admin123":
        return {"error": "Credenciales inválidas"}

    # Token de sesión simulado (en producción sería un JWT)
    token_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.token_operador"

    # 1. Configurar Cookie Segura en la Respuesta
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token_jwt}",
        max_age=7200,        # Expiración en 2 horas (segundos)
        httponly=True,       # Protección XSS (no accesible por JS)
        secure=True,         # Transmisión solo vía HTTPS
        samesite="lax",      # Protección contra CSRF
        path="/"
    )

    # 2. Agregar encabezados personalizados de respuesta
    response.headers["X-Auth-Provider"] = "DataMaq-Security"

    return {"mensaje": "Autenticación exitosa. Cookie de acceso configurada."}

@app.post("/auth/logout", status_code=status.HTTP_200_OK)
def logout(response: Response):
    """
    Elimina la cookie del navegador del cliente.
    """
    response.delete_cookie(key="access_token", path="/")
    return {"mensaje": "Sesión cerrada de forma segura. Cookie eliminada."}
```

---

### 4. Pruebas desde la CLI con HTTPie

```bash
# 1. Ejecutar login e inspeccionar cookies recibidas en la respuesta (--verbose)
http --verbose POST http://127.0.0.1:8000/auth/login username="operador" secret_key="admin123"

# 2. Enviar cookie en peticiones subsiguientes:
http GET http://127.0.0.1:8000/usuario/perfil \
    "Cookie: access_token=Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.token_operador"
```

---

### Resumen de la Lección
`response.set_cookie()` te otorga control total para configurar cookies de respuesta con parámetros de seguridad críticos (`httponly=True`, `secure=True`, `samesite="lax"`), protegiendo tu aplicación frente a vulnerabilidades de tipo XSS y CSRF.
