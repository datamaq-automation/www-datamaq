### 2.6 Módulos, Paquetes y Programación Orientada a Objetos (OOP & Magic Methods)

En aplicaciones profesionales de Python y arquitecturas limpias con FastAPI, el código se organiza en **módulos** y **paquetes**, estructurando el dominio de negocio en clases que encapsulan estado y comportamiento mediante la Programación Orientada a Objetos.

---

### 1. Módulos y Paquetes en Python

- **Módulo**: Cualquier archivo con extensión `.py` que contiene definiciones de funciones, clases y variables.
- **Paquete**: Un directorio que contiene múltiples módulos y un archivo especial **`__init__.py`** (que indica a Python que el directorio debe tratarse como un paquete importable).

```text
mi_proyecto/
├── app/
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   └── models.py
│   └── services/
│       ├── __init__.py
│       └── data_service.py
└── main.py
```

#### Declaraciones de Importación Idiomáticas
```python
# Importar módulo completo
import math
resultado = math.sqrt(16)

# Importar elementos específicos
from app.domain.models import SensorModel

# Importar con alias
import pandas as pd
```

---

### 2. Clases y Objetos en Python

La clase es la plantilla (*blueprint*) para crear objetos que empaquetan atributos (estado) y métodos (comportamiento).

```python
class LecturaSensor:
    """Representa una lectura individual de telemetría industrial."""

    # Constructor del objeto
    def __init__(self, sensor_id: str, valor: float, unidad: str = "V"):
        self.sensor_id = sensor_id
        self.valor = valor
        self.unidad = unidad

    # Método de instancia
    def es_critico(self, umbral: float) -> bool:
        return self.valor > umbral
```

---

### 3. Métodos Mágicos (Dunder Methods)

Los métodos mágicos (comienzan y terminan con doble guion bajo `__`) permiten personalizar cómo se comportan los objetos frente a funciones nativas de Python, representaciones de texto, comparaciones y operadores matemáticos.

#### A. Representación de Objetos (`__str__` y `__repr__`)

- **`__str__`**: Devuelve una representación legible para el usuario final (usado por `print()` y `str()`).
- **`__repr__`**: Devuelve una representación inequívoca e informativa para desarrolladores y depuración (usado por la consola interactiva y logs).

```python
class DispositivoIoT:
    def __init__(self, mac: str, ip: str):
        self.mac = mac
        self.ip = ip

    def __str__(self) -> str:
        return f"Dispositivo IoT [{self.mac}] en IP {self.ip}"

    def __repr__(self) -> str:
        return f"DispositivoIoT(mac='{self.mac}', ip='{self.ip}')"

dev = DispositivoIoT("00:1B:44:11:3A:B7", "192.168.1.50")
print(str(dev))   # Dispositivo IoT [00:1B:44:11:3A:B7] en IP 192.168.1.50
print(repr(dev))  # DispositivoIoT(mac='00:1B:44:11:3A:B7', ip='192.168.1.50')
```

#### B. Métodos de Comparación (`__eq__`, `__lt__`, `__gt__`, etc.)

Permiten comparar dos instancias utilizando los operadores tradicionales (`==`, `<`, `>`, `<=`, `>=`, `!=`):

```python
class LecturaEnergia:
    def __init__(self, sensor_id: str, kwh: float):
        self.sensor_id = sensor_id
        self.kwh = kwh

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, LecturaEnergia):
            return False
        return self.kwh == otro.kwh

    def __lt__(self, otro: "LecturaEnergia") -> bool:
        return self.kwh < otro.kwh

    def __gt__(self, otro: "LecturaEnergia") -> bool:
        return self.kwh > otro.kwh

l1 = LecturaEnergia("s1", 150.5)
l2 = LecturaEnergia("s2", 200.0)

print(l1 == l2)  # False
print(l1 < l2)   # True
```

#### C. Sobrecarga de Operadores Matemáticos (`__add__`, `__sub__`, `__mul__`)

Permite definir el comportamiento de los operadores `+`, `-`, `*` sobre nuestras propias clases:

```python
class MetricaPotencia:
    def __init__(self, kw: float):
        self.kw = kw

    def __add__(self, otra: "MetricaPotencia") -> "MetricaPotencia":
        return MetricaPotencia(self.kw + otra.kw)

    def __sub__(self, otra: "MetricaPotencia") -> "MetricaPotencia":
        return MetricaPotencia(self.kw - otra.kw)

    def __repr__(self) -> str:
        return f"MetricaPotencia({self.kw} kW)"

p1 = MetricaPotencia(120.0)
p2 = MetricaPotencia(80.5)

p_total = p1 + p2
print(p_total)  # MetricaPotencia(200.5 kW)
```

---

### 4. Herencia y Herencia Múltiple (`super()` y MRO)

La **herencia** permite a una clase hija reutilizar código, métodos y atributos de una clase padre.

#### A. Herencia Simple y `super()`
```python
class SensorBase:
    def __init__(self, sensor_id: str, ubicacion: str):
        self.sensor_id = sensor_id
        self.ubicacion = ubicacion

    def obtener_resumen(self) -> str:
        return f"Sensor {self.sensor_id} @ {self.ubicacion}"

class SensorTemperatura(SensorBase):
    def __init__(self, sensor_id: str, ubicacion: str, temp_max_alerta: float):
        # Llama al constructor de la clase padre (SensorBase)
        super().__init__(sensor_id, ubicacion)
        self.temp_max_alerta = temp_max_alerta
```

#### B. Herencia Múltiple y Orden de Resolución de Métodos (MRO)
Python soporta que una clase herede de múltiples clases padre. El orden en el que Python busca métodos heredados se rige por el algoritmo **MRO** (*Method Resolution Order*), el cual se puede inspeccionar con `Clase.mro()`.

```python
class LoggableMixin:
    def log(self, mensaje: str):
        print(f"[LOG {self.__class__.__name__}]: {mensaje}")

class NotificableMixin:
    def notificar(self, msg: str):
        print(f"[NOTIFICACION]: {msg}")

# Herencia Múltiple
class SensorSmart(SensorBase, LoggableMixin, NotificableMixin):
    def procesar_alerta(self, msg: str):
        self.log(msg)
        self.notificar(msg)

sensor_inteligente = SensorSmart("s_smart_01", "Nave_B")
sensor_inteligente.procesar_alerta("Temperatura crítica superada.")
# MRO de la clase
print([c.__name__ for c in SensorSmart.mro()])
# ['SensorSmart', 'SensorBase', 'LoggableMixin', 'NotificableMixin', 'object']
```

---

### Resumen de la Lección
Organizar el código en paquetes y dominar la Programación Orientada a Objetos con métodos mágicos y herencia permite construir modelos de dominio limpios, extensibles y mantenibles en aplicaciones de producción con FastAPI.
