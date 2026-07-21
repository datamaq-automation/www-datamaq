### 2.7 Type Hinting Avanzado y Chequeo Estático con Mypy

El tipado en Python paso de ser una recomendación estética a una herramienta esencial de ingeniería de software gracias al **PEP 484** y al analizador estático de código **`mypy`**. FastAPI utiliza las anotaciones de tipo no solo para autocompletado en el IDE, sino también para realizar validación en tiempo de ejecución a través de Pydantic.

---

### 1. Primeros Pasos con Mypy (Getting Started)

`mypy` es el comprobador estático de tipos estándar para Python. Analiza el código fuente en busca de inconsistencias de tipos sin necesidad de ejecutar la aplicación.

#### Instalación y Ejecución
```bash
pip install mypy
```

Para auditar un script o un paquete de código:
```bash
mypy script.py
# O para auditar todo el código fuente del proyecto:
mypy src/
```

#### Ejemplo de Detección de Errores por Mypy

```python
# script_con_error.py
def calcular_descuento(precio: float, porcentaje: float) -> float:
    return precio * (1.0 - porcentaje)

# Error: se pasa una cadena en lugar de un float
resultado = calcular_descuento("100.0", 0.15)
```

Al ejecutar `mypy script_con_error.py`:
```text
error: Argument 1 to "calcular_descuento" has incompatible type "str"; expected "float"  [arg-type]
```

---

### 2. El Módulo `typing` de Python

El módulo nativo `typing` provee los constructores de tipo necesarios para definir firmas complejas.

#### A. `Any` (Desactivación de Comprobación Estática)
`Any` indica a `mypy` que acepte cualquier tipo de dato sin realizar validaciones sobre él. Debe usarse con precaución para no perder los beneficios del tipado estático.

```python
from typing import Any

def serializar_respuesta(data: Any) -> str:
    # Acepta cualquier objeto y retorna su representación en cadena
    return str(data)
```

#### B. `Callable` (Tipado de Funciones y Callbacks)
Se utiliza para anotar variables o argumentos que reciben funciones o corrutinas. La sintaxis es `Callable[[TiposEntrada], TipoRetorno]`.

```python
from typing import Callable

def ejecutar_procesamiento(
    datos: list[float],
    transformador: Callable[[float], float]
) -> list[float]:
    return [transformador(x) for x in datos]

duplicar: Callable[[float], float] = lambda x: x * 2.0
resultado = ejecutar_procesamiento([10.0, 20.0], duplicar)
```

#### C. `cast` (Forzado Explícito de Tipos)
`cast(TipoTarget, valor)` le indica explícitamente a `mypy` que trate un objeto como si fuera de un tipo específico, sin alterar el objeto en tiempo de ejecución.

```python
from typing import Any, cast

def obtener_configuracion(clave: str) -> Any:
    db_config = {"puerto": 8000, "host": "127.0.0.1"}
    return db_config.get(clave)

# Forzamos a mypy a entender que 'puerto' es un entero
puerto_servidor = cast(int, obtener_configuracion("puerto"))
print(puerto_servidor + 1)  # mypy valida la suma correctamente
```

---

### 3. Tipos Genéricos y Metadata (`TypeVar` y `Annotated`)

- **`TypeVar`**: Permite escribir funciones y clases genéricas conservando el tipo específico recibido.
- **`Annotated`**: Permite adjuntar metadatos descriptivos o restricciones de Pydantic a una anotación de tipo.

```python
from typing import TypeVar, Annotated

T = TypeVar("T")  # Tipo genérico

def obtener_primer_elemento(coleccion: list[T]) -> T | None:
    return coleccion[0] if coleccion else None

# Mypy deduce que 'elem_int' es de tipo int
elem_int = obtener_primer_elemento([10, 20, 30])

# Annotated para validaciones en FastAPI
TemperaturaCelsius = Annotated[float, "Temperatura medida en °C entre -50 y 150"]

def registrar_temperatura(val: TemperaturaCelsius) -> bool:
    return -50.0 <= val <= 150.0
```

---

### Resumen de la Lección
Integrar `mypy` en el flujo de desarrollo previene errores sutiles de tipo antes de llegar a producción. Combinar `Callable`, `Any`, `cast` y `Annotated` otorga flexibilidad máxima para tipar pipelines de datos y controladores web.
