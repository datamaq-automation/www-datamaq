### 1.3 Instalación de Paquetes con pip (Installing Python Packages with pip)

**`pip`** es el gestor de paquetes oficial de Python. Se conecta con el repositorio público **PyPI** (Python Package Index) para descargar e instalar librerías de terceros en tu entorno virtual.

---

### 1. Instalación de Paquetes Básica

Asegúrate de tener tu entorno virtual activo (`source .venv/bin/activate`) antes de instalar librerías.

#### Instalar un Paquete:
```bash
pip install fastapi
```

#### Instalar Múltiples Paquetes Simultáneamente:
```bash
pip install "fastapi[all]" uvicorn pydantic
```

#### Actualizar `pip` a la Última Versión:
```bash
python -m pip install --upgrade pip
```

---

### 2. Archivos de Requisitos (`requirements.txt`)

Para que otros desarrolladores o el servidor de producción puedan replicar exactamente el mismo entorno, documentamos las dependencias en un archivo denominado **`requirements.txt`**.

#### Congelar las Dependencias Actuales:
El comando `pip freeze` genera una lista con las versiones exactas instaladas en el entorno:

```bash
pip freeze > requirements.txt
```

#### Ejemplo de Contenido de `requirements.txt`:
```text
fastapi==0.110.0
uvicorn==0.28.0
pydantic==2.6.4
httpx==0.27.0
```

#### Instalar Dependencias desde `requirements.txt`:
Cuando clonas un proyecto en un equipo nuevo:

```bash
pip install -r requirements.txt
```

---

### 3. Operadores de Versionado en `pip`

| Operador | Ejemplo | Significado |
| :--- | :--- | :--- |
| **`==`** | `fastapi==0.110.0` | Versión exacta fija. |
| **`>=`** | `pydantic>=2.0.0` | Cualquier versión mayor o igual. |
| **`~=`** | `uvicorn~=0.28.0` | Compatible con la versión (acepta `0.28.1`, rechaza `0.29.0`). |

---

### Resumen de la Lección
`pip` y los archivos `requirements.txt` permiten gestionar el ciclo de vida de las dependencias externas de forma reproducible en desarrollo y producción.
