### 1.3 Creación de un entorno virtual de Python

Un **entorno virtual** es un directorio autónomo que contiene una instalación aislada de Python y un conjunto de paquetes independientes del resto del sistema.

#### ¿Por qué es fundamental el aislamiento en Data Science?

En proyectos de Machine Learning e ingeniería de software, las dependencias pueden volverse complejas rápidamente. Instalar paquetes de forma global en el sistema puede provocar conflictos de versiones incompatibles entre librerías (por ejemplo, si un proyecto requiere Pydantic v1 y otro Pydantic v2). 

Crear un entorno virtual garantiza la reproducibilidad de tu proyecto tanto en tu máquina local como en el servidor de producción o contenedor Docker.

#### Paso 1: Crear el Entorno Virtual con venv

Navega a la carpeta de tu proyecto y ejecuta el módulo nativo `venv` de Python:

```bash
# Crear un directorio para el proyecto
mkdir fastapi-ml-app
cd fastapi-ml-app

# Crear el entorno virtual en una carpeta oculta llamada .venv
python -m venv .venv
```

#### Paso 2: Activar el Entorno Virtual

La forma de activación depende de tu sistema operativo:

**En Linux / macOS (Bash o Zsh):**
```bash
source .venv/bin/activate
```

**En Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**En Windows (Command Prompt - CMD):**
```cmd
.venv\Scripts\activate.bat
```

Una vez activado, verás el nombre del entorno `(.venv)` reflejado al principio del prompt de tu terminal.

#### Paso 3: Verificación de la Activación

Comprueba que la ruta del ejecutable de Python apunta hacia el interior de la carpeta `.venv`:

```bash
which python
# Resultado esperado: /ruta/a/tu/proyecto/fastapi-ml-app/.venv/bin/python
```

#### Paso 4: Buenas Prácticas y Control de Versiones

Si utilizas Git en tu proyecto, asegúrate de **nunca subir la carpeta del entorno virtual al repositorio**. Para ello, crea o edita el archivo `.gitignore`:

```ini
# .gitignore
.venv/
__pycache__/
*.pyc
.env
```

#### Desactivación del Entorno

Cuando termines de trabajar en tu proyecto, podés salir del entorno virtual simplemente ejecutando:

```bash
deactivate
```
