### 3.5 Documentación OpenAPI y Pruebas CLI (Swagger UI & HTTPie)

Una de las características más apreciadas de FastAPI es la generación automática y estandarizada de documentación interactiva basada en la especificación **OpenAPI** (anteriormente Swagger) y **JSON Schema**.

---

### 1. Documentación Interactiva en el Navegador

Sin instalar herramientas adicionales, al iniciar tu aplicación con Uvicorn (`uvicorn main:app --reload`), FastAPI genera automáticamente dos interfaces de documentación interactiva:

#### A. Swagger UI (`/docs`)
Ingresando en tu navegador a [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs):
- Visualizarás todos los endpoints agrupados por etiquetas (`tags`).
- Podrás desplegar cada operación, inspeccionar los esquemas JSON de entrada/salida y hacer clic en el botón **"Try it out"** para ejecutar peticiones HTTP directamente desde la web.

#### B. ReDoc (`/redoc`)
Ingresando a [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc):
- Interfaz elegante de tres columnas orientada a documentación técnica y referencia de arquitecturas REST.

---

### 2. Pruebas de Endpoints desde la CLI con HTTPie y Curl

Aunque Swagger UI permite probar desde el navegador, la línea de comandos con **HTTPie** (`http`) o `curl` es el método preferido para automatizar pruebas en scripts.

#### A. Petición GET simple
```bash
http GET http://127.0.0.1:8000/health
```

#### B. Petición GET con Query Parameters
```bash
http GET http://127.0.0.1:8000/mediciones planta=="Avellaneda" limit:=5
```

#### C. Petición POST enviando un Request Body en JSON
HTTPie serializa automáticamente pares `clave=valor` a JSON:

```bash
http POST http://127.0.0.1:8000/inferencia/predict \
    sensor_id="Sensor_Motor_01" \
    temperatura:=85.4 \
    presion:=12.5
```

*Respuesta recibida en consola:*
```text
HTTP/1.1 201 Created
content-type: application/json

{
    "diagnostico": "ALERTA",
    "id": 1,
    "input": {
        "presion": 12.5,
        "sensor_id": "Sensor_Motor_01",
        "temperatura": 85.4,
        "vibracion": null
    },
    "score_riesgo": 0.417
}
```

---

### Resumen del Capítulo 3
Has aprendido a construir una API RESTful completa en FastAPI, capturar datos mediante *Path Parameters*, *Query Parameters* y *Request Body*, auditarla mediante Swagger UI (`/docs`) y realizar pruebas profesionales desde la terminal con HTTPie.
