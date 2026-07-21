### 1.2 Creación de Entornos Virtuales en Python (Creating a Virtual Environment)

Un **entorno virtual** es una estructura de directorio aislada que contiene una instalación propia de Python e intérpretes, junto con sus librerías y dependencias específicas.

---

### 1. ¿Por qué son indispensables los Entornos Virtuales?

Imaginá que estás trabajando en dos proyectos de Ciencia de Datos en el mismo equipo:
- El **Proyecto A** requiere `FastAPI 0.95.0` y `Pydantic 1.10.0`.
- El **Proyecto B** requiere `FastAPI 0.110.0` y `Pydantic 2.6.0`.

Si instalaras los paquetes de forma global en el sistema, la instalación de un proyecto sobrescribiría las librerías del otro. Los entornos virtuales resuelven este problema aislando las dependencias por proyecto.

---

### 2. Creación de un Entorno Virtual con `venv`

Python incluye el módulo nativo **`venv`** para la generación de entornos virtuales sin necesidad de instalar herramientas externas.

#### Comandos para Crear y Activar el Entorno Virtual:

Navegá al directorio raíz de tu proyecto en la terminal y ejecutá:

```bash
# 1. Crear el entorno virtual en una carpeta oculta llamada .venv
python -m venv .venv
```

#### Activar el Entorno Virtual:

- **En Linux / macOS (Bash / Zsh):**
  ```bash
  source .venv/bin/activate
  ```

- **En Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

#### Indicador en la Terminal:
Una vez activado, el prompt de tu terminal mostrará el nombre del entorno virtual al inicio:
```text
(.venv) agustin@datamaq:~/proyectos_software/mi-api$
```

---

### 3. Desactivación e Ignorado en Control de Versiones

#### Desactivar el Entorno Virtual:
Para salir del entorno virtual y volver al intérprete global de la terminal, ejecutá:
```bash
deactivate
```

#### Ignorar el Entorno Virtual en Git (`.gitignore`):
**¡Regla de Oro!**: Jamás se debe incluir la carpeta `.venv` en el repositorio Git. Agregá la carpeta a tu archivo `.gitignore`:

```text
# Archivo .gitignore
.venv/
__pycache__/
*.pyc
```

---

### Resumen de la Lección
Los entornos virtuales con `venv` garantizan que las librerías instaladas pertenezcan exclusivamente a tu proyecto, asegurando reproducibilidad y aislamiento total.
