### 1.2 Instalación de una distribución de Python usando pyenv

Utilizaremos **pyenv** para gestionar múltiples versiones de Python de manera aislada en nuestro sistema sin interferir con el Python nativo del sistema operativo.

#### ¿Por qué usar pyenv?

En proyectos de ciencia de datos y desarrollo backend, es común que distintos proyectos requieran diferentes versiones secundarias de Python (por ejemplo, Python 3.10 para cierta librería legacy y Python 3.12 para FastAPI en producción). `pyenv` nos permite instalar, cambiar y fijar versiones de Python específicas por proyecto de manera limpia y transparente.

#### Paso 1: Instalación de Dependencias de Compilación

Antes de instalar `pyenv`, debemos asegurarnos de contar con las librerías del sistema necesarias para compilar Python desde la fuente:

**En Ubuntu / Debian:**
```bash
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl git \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

**En macOS (con Homebrew):**
```bash
brew install openssl readline sqlite3 xz zlib tcl-tk
```

#### Paso 2: Instalación de pyenv

Instala `pyenv` utilizando el script de instalación automática oficial:

```bash
curl https://pyenv.run | bash
```

#### Paso 3: Configurar las Variables de Entorno del Shell

Agrega las siguientes líneas a tu archivo de configuración del shell (`~/.bashrc` para Bash o `~/.zshrc` para Zsh):

```bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

Aplica los cambios en tu sesión actual:

```bash
source ~/.bashrc  # o source ~/.zshrc
```

#### Paso 4: Instalación de la Versión Recomendada de Python

Instalaremos la versión recomendada para el curso (**Python 3.12.0**):

```bash
# Listar las versiones disponibles
pyenv install --list | grep "3.12"

# Instalar la versión 3.12.0
pyenv install 3.12.0

# Establecer la versión global o local del proyecto
pyenv global 3.12.0
```

#### Verificación

Verifica que la versión activa sea la instalada por `pyenv`:

```bash
python --version
# Debería mostrar: Python 3.12.0

which python
# Debería apuntar a: ~/.pyenv/shims/python
```

En la siguiente lección crearemos un entorno virtual dedicado exclusivamente a los paquetes de nuestro backend FastAPI.
