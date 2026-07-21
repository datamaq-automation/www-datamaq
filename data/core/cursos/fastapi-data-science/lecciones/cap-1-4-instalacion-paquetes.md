### 1.4 Instalación de paquetes de Python con pip

Con nuestro entorno virtual activado, utilizaremos **pip** (el administrador de paquetes oficial de Python) para instalar FastAPI, Uvicorn y Pydantic.

#### Paso 1: Actualizar pip a la Última Versión

Antes de instalar dependencias externas, es una buena práctica asegurar que `pip`, `setuptools` y `wheel` estén actualizados:

```bash
python -m pip install --upgrade pip setuptools wheel
```

#### Paso 2: Instalación de las Librerías Núcleo

Instalaremos las dependencias requeridas para construir y servir nuestra API:

```bash
pip install fastapi "uvicorn[standard]" pydantic
```

#### Descripción de las Librerías Instaladas:

1. **FastAPI**: El framework web moderno y de alto rendimiento especializado en la creación de APIs RESTful asíncronas con Python.
2. **Uvicorn `[standard]`**: Servidor web ASGI de altísima velocidad basado en `uvloop` y `httptools` para ejecutar aplicaciones asíncronas de Python en producción.
3. **Pydantic**: El motor de validación de datos, parsing y conversión de tipos en tiempo de ejecución utilizado internamente por FastAPI.

#### Paso 3: Instalación de Librerías Complementarias para Ciencia de Datos

Para las lecciones posteriores de integración de modelos de Machine Learning, instalaremos también las siguientes utilidades:

```bash
pip install numpy pandas scikit-learn joblib httpx
```

- **numpy & pandas**: Manipulación y transformación de matrices y DataFrames.
- **scikit-learn & joblib**: Carga y ejecución de modelos de Machine Learning pre-entrenados.
- **httpx**: Cliente HTTP asíncrono que utilizaremos para realizar pruebas unitarias sobre nuestra aplicación FastAPI.

#### Paso 4: Generación de requirements.txt

Para congelar las versiones de las librerías instaladas y garantizar que otros desarrolladores o el servidor de producción descarguen exactamente las mismas dependencias, genera el archivo `requirements.txt`:

```bash
pip freeze > requirements.txt
```

Puedes inspeccionar el contenido del archivo generado:

```bash
cat requirements.txt
```

Para reinstalar todas las dependencias en un entorno nuevo, bastará con ejecutar:

```bash
pip install -r requirements.txt
```
