### Inyección de Dependencias en FastAPI con Depends

La **Inyección de Dependencias** (Dependency Injection - DI) es un patrón de diseño de software que permite escribir código modular, mantenible y fácilmente testeable. FastAPI incluye un sistema de inyección de dependencias extraordinariamente potente y fácil de usar mediante la función `fastapi.Depends`.

---

### 1. ¿Por qué utilizar Inyección de Dependencias?

En desarrollos web tradicionales, los controladores o endpoints crean internamente sus propias conexiones a bases de datos, instancian clasificadores de Machine Learning o leen tokens de autenticación. Esto genera un alto acoplamiento y dificulta la reutilización de código y la escritura de pruebas unitarias.

El sistema de dependencias de FastAPI resuelve esto permitiendo:
- **Reutilizar lógica compartida** (paginación, autenticación, conexión a bases de datos).
- **Gestionar el ciclo de vida de recursos** (abrir y cerrar conexiones de forma segura).
- **Inyectar Mocks / Stubs en pruebas** utilizando `app.dependency_overrides`.

---

### 2. Dependencia Básica basada en Funciones

Una dependencia es simplemente una función (o clase invocable) que acepta los mismos parámetros que cualquier función de ruta de FastAPI:

```python
from fastapi import FastAPI, Depends, Query

app = FastAPI()

# Dependencia para parámetros de paginación
def parametros_paginacion(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(10, ge=1, le=100, description="Límite por página")
):
    return {"skip": skip, "limit": limit}

@app.get("/dataset/lecturas")
def obtener_lecturas(pagination: dict = Depends(parametros_paginacion)):
    # Los valores de skip y limit son validados automáticamente por la dependencia
    return {
        "mensaje": f"Retornando desde {pagination['skip']} hasta {pagination['skip'] + pagination['limit']}",
        "params": pagination
    }
```

---

### 3. Carga Eficiente (Singleton) de Modelos de Machine Learning

Cargar un modelo de Inteligencia Artificial de 500 MB en disco dentro de la función del endpoint para cada petición provocaría latencias inaceptables de varios segundos y saturaría la memoria RAM.

Utilizando una clase dependencia con estado, podemos asegurar que el modelo se cargue una sola vez en memoria (patrón Singleton):

```python
import joblib
from typing import Any
from fastapi import FastAPI, Depends

class MLModelPredictorService:
    def __init__(self):
        # Simulación de carga diferida del modelo entrenado
        print("Cargando modelo de Scikit-Learn en memoria...")
        self.model = {"version": "v1.2", "weights": [0.5, 0.3, 0.2]}

    def predict(self, features: list[float]) -> float:
        # Predicción rápida utilizando los pesos cargados
        return sum(f * w for f, w in zip(features, self.model["weights"]))

# Instancia global del servicio
predictor_service = MLModelPredictorService()

# Función de dependencia que retorna el servicio listo
def get_predictor_service() -> MLModelPredictorService:
    return predictor_service

@app.post("/inferencia")
def ejecutar_inferencia(
    features: list[float],
    service: MLModelPredictorService = Depends(get_predictor_service)
):
    score = service.predict(features)
    return {"score": score, "model_version": service.model["version"]}
```

---

### 4. Gestor de Recursos con `yield` (Context Managers)

Cuando una dependencia requiere inicializar un recurso (por ejemplo, abrir una conexión a la base de datos) y luego limpiarlo/cerrarlo una vez procesada la respuesta HTTP, se utiliza la sintaxis `yield`:

```python
from typing import AsyncGenerator

async def get_db_session() -> AsyncGenerator:
    db = {"session_id": "xyz-123", "active": True}
    try:
        print("-> Abriendo sesión de Base de Datos")
        yield db
    finally:
        print("<- Cerrando sesión de Base de Datos")
        db["active"] = False
```

---

### 5. Pruebas Unitarias con `app.dependency_overrides`

Una de las mayores ventajas de la inyección de dependencias es la capacidad de reemplazar dependencias reales por versiones simuladas (Mocks) en los tests unitarios con `pytest`:

```python
from fastapi.testclient import TestClient

# Mock de la dependencia para testing
def mock_get_predictor_service():
    class FakePredictor:
        def predict(self, features):
            return 0.99
        model = {"version": "test-mock"}
    return FakePredictor()

# Reemplazar la dependencia real por el Mock
app.dependency_overrides[get_predictor_service] = mock_get_predictor_service

client = TestClient(app)

def test_inferencia_endpoint():
    response = client.post("/inferencia", json=[1.0, 2.0, 3.0])
    assert response.status_code == 200
    assert response.json()["score"] == 0.99
    
# Limpiar los overrides al finalizar
app.dependency_overrides.clear()
```

La inyección de dependencias es la herramienta fundamental para construir arquitecturas limpias y desacopladas en aplicaciones profesionales con FastAPI.
