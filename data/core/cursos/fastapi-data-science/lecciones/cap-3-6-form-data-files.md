### 3.6 Datos de Formularios y Carga de Archivos (Form Data & File Uploads)

En muchas aplicaciones de Ciencia de Datos e Inteligencia Artificial es necesario recibir **datos de formularios HTML** (`application/x-www-form-urlencoded`) y **archivos adjuntos** (`multipart/form-data`), tales como imágenes, datasets CSV o archivos binarios de modelos de Machine Learning.

> **Requisito Previo**: Para procesar formularios y carga de archivos, FastAPI requiere la instalación de la librería `python-multipart`:
> ```bash
> pip install python-multipart
> ```

---

### 1. Datos de Formularios (`Form`)

Cuando el cliente envía datos desde un formulario web tradicional en lugar de un JSON, utilizamos la función **`Form()`** de FastAPI:

```python
from fastapi import FastAPI, Form, status

app = FastAPI(title="API de Formularios")

@app.post("/login", status_code=status.HTTP_200_OK)
def iniciar_sesion(
    username: str = Form(..., description="Nombre de usuario"),
    password: str = Form(..., description="Contraseña de acceso")
):
    """
    Recibe los datos en formato application/x-www-form-urlencoded
    """
    return {
        "usuario": username,
        "status": "autenticado"
    }
```

---

### 2. Carga de Archivos (`File` vs `UploadFile`)

FastAPI ofrece dos alternativas para recibir archivos en el servidor:

#### A. Carga Directa en Memoria con `bytes` (`File`)
Lee todo el contenido del archivo en memoria RAM como una secuencia de `bytes`. Se recomienda **únicamente para archivos muy pequeños** (menores a 1 MB):

```python
from fastapi import FastAPI, File

app = FastAPI()

@app.post("/files/small-bytes")
def recibir_archivo_pequeno(file_bytes: bytes = File(...)):
    return {"tamanio_bytes": len(file_bytes)}
```

#### B. Carga Eficiente con `UploadFile` (**Recomendado**)
`UploadFile` utiliza un objeto archivo temporal en disco (*spooled file*) que no sobrecarga la memoria RAM. Provee métodos asíncronos (`.read()`, `.write()`, `.seek()`, `.close()`) y metadatos del archivo:

- `filename`: Nombre original del archivo enviado por el cliente.
- `content_type`: Tipo MIME (ejemplo: `text/csv`, `image/png`, `application/pdf`).
- `file`: Objeto de archivo Python subyacente.

```python
from fastapi import FastAPI, File, UploadFile, status

app = FastAPI()

@app.post("/dataset/upload", status_code=status.HTTP_201_CREATED)
async def subir_dataset_csv(file: UploadFile = File(...)):
    """
    Recibe un archivo CSV o dataset sin cargar todo el archivo en la RAM.
    """
    # Validar extensión o tipo MIME
    if not file.filename.endswith(".csv"):
        return {"error": "Solo se permiten archivos con extensión .csv"}
        
    # Leer los primeros 1024 bytes para inspección
    primeros_bytes = await file.read(1024)
    await file.seek(0)  # Rebobinar el puntero al inicio
    
    return {
        "nombre_archivo": file.filename,
        "tipo_content": file.content_type,
        "preview_bytes": len(primeros_bytes)
    }
```

---

### 3. Combinando Formularios y Carga de Archivos (`Form` + `UploadFile`)

En proyectos de Machine Learning es habitual recibir metadatos en campos de formulario junto al archivo del modelo o dataset:

```python
from fastapi import FastAPI, Form, File, UploadFile, status

app = FastAPI()

@app.post("/modelos/entrenar")
async def registrar_y_cargar_modelo(
    nombre_modelo: str = Form(..., description="Nombre del modelo de ML"),
    version: str = Form("1.0.0"),
    archivo_weights: UploadFile = File(..., description="Archivo de pesos .pkl o .onnx")
):
    """
    Recibe campos multipart/form-data combinando formulario y archivo.
    """
    contenido = await archivo_weights.read()
    
    return {
        "modelo": nombre_modelo,
        "version": version,
        "archivo": archivo_weights.filename,
        "tamanio_kb": round(len(contenido) / 1024, 2)
    }
```

---

### 4. Carga de Múltiples Archivos (`list[UploadFile]`)

Para permitir que el usuario seleccione y suba múltiples archivos en una sola petición:

```python
@app.post("/dataset/lote")
async def subir_lote_datasets(archivos: list[UploadFile] = File(...)):
    reporte = []
    for f in archivos:
        contenido = await f.read()
        reporte.append({
            "filename": f.filename,
            "bytes": len(contenido)
        })
    return {"total_archivos": len(archivos), "archivos": reporte}
```

---

### 5. Pruebas desde la CLI con HTTPie

Para probar la carga de formularios y archivos desde la terminal utilizando **HTTPie**:

```bash
# 1. Enviar formulario application/x-www-form-urlencoded:
http --form POST http://127.0.0.1:8000/login username="operador1" password="secretpassword"

# 2. Subir un archivo con multipart/form-data:
http --form POST http://127.0.0.1:8000/dataset/upload file@./datos_sensores.csv

# 3. Combinar campos de formulario y archivo:
http --form POST http://127.0.0.1:8000/modelos/entrenar \
    nombre_modelo="XGBoost_Vibracion" \
    version="2.1.0" \
    archivo_weights@./modelo.pkl
```

---

### Resumen de la Lección
Con `Form()` y `UploadFile` podés construir endpoints capaces de recibir formularios multipart y gestionar grandes volúmenes de archivos o datasets industriales sin saturar la memoria del servidor.
