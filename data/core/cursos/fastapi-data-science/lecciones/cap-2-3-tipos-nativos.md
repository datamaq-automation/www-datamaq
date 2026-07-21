### 2.3 Tipos de Datos Nativos y Lógica Booleana (Built-in Types & Boolean Logic)

Python provee un conjunto integrado de tipos de datos fundamentales (*built-in types*). Comprender sus propiedades numéricas, inmutabilidad, operadores lógicos y métodos de comprobación de existencia es esencial para construir modelos de datos y procesar cargas en FastAPI.

---

### 1. Los 6 Tipos Nativos Fundamentales

| Tipo | Descripción | Ejemplo de Literal | Mutabilidad |
| :--- | :--- | :--- | :--- |
| **`int`** | Enteros de precisión arbitraria | `42`, `-1050` | Inmutable |
| **`float`** | Números de coma flotante (IEEE 754 64-bit) | `3.14159`, `1e-5` | Inmutable |
| **`complex`** | Números complejos (real + imaginario) | `3 + 4j`, `2.5j` | Inmutable |
| **`bool`** | Valores booleanos de verdad | `True`, `False` | Inmutable |
| **`str`** | Secuencia inmutable de caracteres Unicode | `"DataMaq"`, `'IoT'` | Inmutable |
| **`NoneType`** | Representa la ausencia de valor (`None`) | `None` | Inmutable |

---

### 2. Lógica Booleana y Comprobación de Existencia (Existence & Membership)

#### A. Operadores Lógicos (`and`, `or`, `not`)
Python utiliza palabras en inglés legibles para la evaluación lógica:

```python
sistema_activo = True
mantenimiento_programado = False
presion_critica = True

# Evaluación lógica combinada
alerta_activada = (presion_critica or sistema_activo) and not mantenimiento_programado
print(f"Alerta: {alerta_activada}")  # True
```

#### B. Comprobación de Existencia (`in` y `not in`)
El operador **`in`** (y su inverso **`not in`**) permite verificar si un elemento o subcadena se encuentra presente en una estructura de datos o cadena:

```python
# 1. Búsqueda de subcadena en texto
log_line = "ERROR 2026-07-21 15:42:01 - Falla de sensor de temperatura en Motor_01"

if "ERROR" in log_line:
    print("Se detectó un evento crítico en los logs.")

# 2. Búsqueda de clave en diccionarios
telemetria = {"temperatura": 85.4, "presion": 2.1}

if "vibracion" not in telemetria:
    telemetria["vibracion"] = 0.0  # Asignar valor por defecto

# 3. Búsqueda en listas o conjuntos
sensores_permitidos = {"s1", "s2", "s3"}
if "s4" not in sensores_permitidos:
    print("Sensor s4 no está registrado en la lista blanca.")
```

#### C. Evaluación de Verdad (Truthy / Falsy)

En Python, todos los objetos se pueden evaluar en contextos booleanos:

- **Valores *Falsy*** (se evalúan a `False`): `False`, `None`, `0`, `0.0`, `""`, `[]`, `{}`, `set()`.
- **Valores *Truthy*** (se evalúan a `True`): Cualquier número distinto de cero, cadenas no vacías y colecciones con elementos.

```python
def validar_endpoint(url: str | None, reintentos: int) -> bool:
    # 'not url' es True si url es None o ""
    if not url or reintentos <= 0:
        return False
    return True
```

---

### 3. Cadenas de Texto (`str`) y Nulos (`NoneType`)

#### Métodos de Cadenas para Procesamiento de Datos
Las cadenas en Python son secuencias Unicode inmutables con métodos nativos esenciales:

```python
raw_data = "  sensor_tanque_02:450.8:NORMAL \n"

# Limpieza y parsing
clean_data = raw_data.strip()
componentes = clean_data.split(":")  # ['sensor_tanque_02', '450.8', 'NORMAL']

tag_sensor, lectura_str, estado = componentes
lectura_flotante = float(lectura_str)

# Formateo interpolado (f-strings)
reporte = f"Sensor: {tag_sensor.upper()} | Lectura: {lectura_flotante:.2f} Lts | Estado: {estado}"
```

#### Uso Idiomático de `None`
`None` representa la ausencia de valor. Su comprobación debe hacerse usando el operador de identidad **`is`** o **`is not`**:

```python
def consultar_offset_sensor(sensor_id: str) -> float | None:
    tabla_offsets = {"s1": 1.05}
    return tabla_offsets.get(sensor_id)

offset = consultar_offset_sensor("s2")

if offset is None:
    print("Sin offset configurado. Utilizando 0.0 por defecto.")
```

---

### Resumen de la Lección
La lógica booleana, las comprobaciones de existencia (`in` / `not in`) y los tipos nativos son los bloques constitutivos para escribir validadores y condiciones de negocio en FastAPI.
