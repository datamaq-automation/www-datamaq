### 1.1 Instalación de una Distribución de Python con pyenv (Installing Python Using pyenv)

En proyectos profesionales de desarrollo de software y Ciencia de Datos, confiar en la versión de Python preinstalada en el sistema operativo (System Python) no es recomendable: puede estar desactualizada, carecer de librerías de desarrollo o causar conflictos catastróficos si se modifican sus paquetes globales.

La herramienta estándar para instalar y alternar entre múltiples versiones de Python de forma aislada y limpia es **`pyenv`**.

---

### 1. ¿Qué es `pyenv` y por qué utilizarlo?

**`pyenv`** permite:
- Instalar múltiples versiones de Python en el espacio de usuario (sin requerir permisos de administrador `root` o `sudo`).
- Establecer una versión global por defecto para el usuario.
- Fijar una versión específica de Python por proyecto (`pyenv local 3.10.12`).
- Evitar contaminar la instalación de Python del sistema operativo.

---

### 2. Instalación de `pyenv` en Linux / macOS

#### A. Requisitos previos en Ubuntu / Debian:
Antes de compilar versiones de Python con `pyenv`, instalamos las dependencias del sistema:

```bash
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

#### B. Ejecutar el Instalador Automático de pyenv:
```bash
curl https://pyenv.run | bash
```

#### C. Configurar las variables de entorno en tu Shell (`~/.bashrc` o `~/.zshrc`):
Agregá las siguientes líneas al final de tu archivo de configuración de terminal:

```bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

Reiniciá tu terminal o ejecutá `source ~/.bashrc` para aplicar los cambios.

---

### 3. Comandos Esenciales de `pyenv`

#### Listar versiones disponibles para instalar:
```bash
pyenv install --list | grep " 3.10"
```

#### Instalar una versión específica de Python:
```bash
pyenv install 3.10.12
```

#### Listar las versiones instaladas en tu equipo:
```bash
pyenv versions
```

#### Configurar la versión de Python para el proyecto actual:
Navegá al directorio de tu proyecto y ejecutá:

```bash
pyenv local 3.10.12
```

Esto creará un archivo oculto `.python-version` en la raíz del proyecto. Cada vez que ingreses a esa carpeta, `pyenv` activará automáticamente la versión de Python indicada.

---

### Resumen de la Lección
Con `pyenv` asegurás que todo el equipo de desarrollo trabaje con la misma versión exacta de Python sin colisionar con el sistema operativo.
