### 2.8 Programación Asíncrona (Async I/O) y Resumen del Capítulo

La programación asíncrona es la característica arquitectónica clave que permite a **FastAPI** competir en velocidad de procesamiento y concurrencia con entornos como Node.js o Go, utilizando un único hilo principal.

---

### 1. ¿Qué es Asynchronous I/O (Async I/O)?

En servidores web tradicionales síncronos (WSGI), cuando una petición HTTP requiere consultar una base de datos o realizar una llamada de red externa, el hilo de ejecución queda **bloqueado** esperando la respuesta.

**Async I/O (ASGI)** introduce el concepto de **I/O no bloqueante**:
- Mientras una petición espera que el disco o la red respondan, el procesador no queda ocioso.
- El **Event Loop** (bucle de eventos) cede el control inmediatamente a otra petición entrante, procesando miles de solicitudes simultáneas de forma altamente eficiente.

---

### 2. Conceptos Clave: `async`, `await` y el Event Loop

- **`async def`**: Declara una función corrutina asíncrona. Al ser invocada, no ejecuta el código inmediatamente, sino que retorna un objeto *coroutine*.
- **`await`**: Pausa la ejecución de la corrutina actual y entrega el control de vuelta al Event Loop hasta que la operación asíncrona se complete.
- **`asyncio`**: El módulo de la librería estándar de Python que provee el Event Loop y primitivas para gestionar tareas concurrentes.

```python
import asyncio
from fastapi import FastAPI

app = FastAPI()

# Simulación de servicio I/O no bloqueante
async def realizar_consulta_db_async(query_id: str) -> dict:
    # await asyncio.sleep() cede la ejecución al Event Loop sin bloquear el proceso
    await asyncio.sleep(0.1)
    return {"query_id": query_id, "resultado": "OK", "filas_procesadas": 150}

@app.get("/api/v1/reporte/{query_id}")
async def get_reporte(query_id: str):
    datos = await realizar_consulta_db_async(query_id)
    return {"status": "success", "data": datos}
```

---

### 3. Tareas Asíncronas vs Tareas Bloqueantes (CPU-Bound)

> **Regla de Oro para FastAPI**:
> 1. Utilizá `async def` cuando invoques librerías preparadas para I/O asíncrono (ej. `httpx`, `asyncpg`, `motor` para MongoDB, `aioredis`).
> 2. Utilizá `def` síncrono estándar cuando realices procesamiento intensivo de CPU (ej. inferencia con `scikit-learn`, manipulaciones con `pandas` o matrices con `numpy`). FastAPI detectará automáticamente las funciones `def` y las ejecutará en un **ThreadPool secundario**, evitando congelar el Event Loop principal.

---

### 4. Resumen Integrador del Capítulo 2

En este capítulo exploramos exhaustivamente las especificidades del lenguaje Python necesarias para dominar el desarrollo moderno en FastAPI:

1. **Fundamentos y Ejecución**: Comprendimos el modelo de compilación a Bytecode y la PVM, el tipado dinámico y fuerte, el soporte multiparadigma y la estructura de entrada mediante `if __name__ == "__main__":`.
2. **Indentación Estricta**: La regla de 4 espacios (PEP 8) como pilar de legibilidad y control de ámbitos.
3. **Tipos Nativos y Lógica Booleana**: Manejo de `int`, `float`, `complex`, `bool`, `str`, `NoneType` y operadores de pertenencia (`in`, `not in`).
4. **Estructuras de Datos**: Diferencias computacionales entre `list`, `tuple`, `dict` y `set`.
5. **Flujo de Control y Funciones**: Bucles `while` y `for`, control fino con `break`/`continue`, y la potencia de parámetros dinámicos `*args` y `**kwargs`.
6. **Módulos, Paquetes y OOP**: Organización modular (`__init__.py`), clases, métodos mágicos (`__str__`, `__repr__`, `__eq__`, `__add__`) y herencia múltiple con `super()` y MRO.
7. **Type Hints y Async I/O**: Verificación estática con `mypy` y la arquitectura no bloqueante con `async/await`.

¡Estás listo para avanzar a la **Sección B** y construir tu primera API RESTful completa con FastAPI!
