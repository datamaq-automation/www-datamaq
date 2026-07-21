### 1.4 Instalación de la Utilidad HTTPie (Installing HTTPie)

Durante el desarrollo de APIs RESTful con FastAPI, es fundamental contar con un cliente HTTP ágil en la línea de comandos para realizar pruebas rápidas sin depender del navegador web.

**HTTPie** (`http` / `https`) es un cliente de consola moderno, legible y con coloreado sintáctico automático diseñado específicamente para desarrolladores.

---

### 1. ¿Por qué HTTPie frente a `curl`?

A diferencia del comando tradicional `curl`, **HTTPie**:
- Formatea e indenta automáticamente las respuestas JSON devueltas por la API.
- Aplica resaltado de sintaxis con colores en la terminal.
- Envía payloads JSON mediante una sintaxis limpia y natural (`clave=valor` o `clave:=numero`).
- Simplifica el envío de cabeceras HTTP y datos de formulario.

---

### 2. Instalación de HTTPie

Podemos instalar HTTPie directamente mediante `pip` dentro de nuestro entorno virtual o utilizando el gestor de paquetes del sistema operativo:

#### Opción A: Instalación vía `pip` (Recomendado en el entorno virtual):
```bash
pip install httpie
```

#### Opción B: Instalación vía `apt` (Ubuntu / Debian):
```bash
sudo apt update && sudo apt install -y httpie
```

#### Opción C: Instalación vía Homebrew (macOS):
```bash
brew install httpie
```

---

### 3. Ejemplos de Uso de HTTPie

Una vez instalado, el comando ejecutable en la terminal es **`http`**:

#### A. Petición GET simple:
```bash
http GET http://127.0.0.1:8000/
```

#### B. Petición GET con Parámetros de Consulta (Query Parameters):
```bash
http GET http://127.0.0.1:8000/equipos planta=="Avellaneda" limit:=5
```

#### C. Petición POST enviando un Payload JSON:
HTTPie convierte los pares `clave=valor` automáticamente a formato JSON:

```bash
http POST http://127.0.0.1:8000/sensor/lectura \
    sensor_id="S-101" \
    temperatura:=42.5 \
    activo:=true
```

#### D. Inspeccionar Cabeceras de Respuesta (`--verbose`):
```bash
http --verbose GET http://127.0.0.1:8000/health
```

---

### Resumen de la Lección
HTTPie es una herramienta de terminal indispensable para auditar, probar y depurar peticiones HTTP hacia tu API en FastAPI con sintaxis limpia y JSON coloreado.
