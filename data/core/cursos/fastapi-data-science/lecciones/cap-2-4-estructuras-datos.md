### 2.4 Estructuras de Datos (List, Tuples, Dictionaries & Sets)

Las estructuras de datos integradas de Python permiten organizar, filtrar y transformar colecciones complejas. La elección correcta de la estructura condiciona el rendimiento computacional (complejidad temporal $O(1)$ vs $O(n)$) y la seguridad de los datos.

---

### 1. Cuadro Comparativo de Estructuras Integradas

| Estructura | Sintaxis | Mutabilidad | Ordenada | Permite Duplicados | Búsqueda por Clave/Índice |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **List** (`list`) | `[1, 2, 3]` | **Mutablemente dinámica** | Sí | Sí | Por índice entero `O(1)` |
| **Tuple** (`tuple`) | `(1, 2, 3)` | **Inmutable** | Sí | Sí | Por índice entero `O(1)` |
| **Dictionary** (`dict`) | `{"k": "v"}` | **Mutablemente dinámica** | Sí (Python 3.7+) | Claves únicas | Por clave `O(1)` hash table |
| **Set** (`set`) | `{1, 2, 3}` | **Mutablemente dinámica** | No | **No (Únicos)** | Por pertenencia `val in set` `O(1)` |

---

### 2. Listas (`list`): Colecciones Mutables Ordenadas

Las listas permiten almacenar secuencias de elementos heterogéneos.

```python
# Operaciones fundamentales
muestras = [10.5, 12.0, 15.8, 9.2]

muestras.append(14.1)         # Agregar al final
muestras[0] = 11.0            # Modificar elemento
ultimo = muestras.pop()       # Extraer y retornar el último -> 14.1

# Slicing (Rebanado: [inicio:fin:paso])
sub_muestras = muestras[1:3]  # [12.0, 15.8]
invertidas = muestras[::-1]   # Invertir lista completa
```

---

### 3. Tuplas (`tuple`): Secuencias Inmutables Protegidas

Las tuplas son ideales para agrupar datos de estructura fija que no deben ser modificados durante la ejecución de la aplicación (garantizando inmutabilidad y menor consumo de memoria).

```python
# Definición de coordenadas o configuraciones fijas
ubicacion_sensor = (-34.6037, -58.3816, "Planta_Avellaneda")

# Desempaquetado de tuplas (Tuple Unpacking)
lat, lon, planta = ubicacion_sensor
print(f"Sensor ubicado en {planta}: Lat {lat}, Lon {lon}")

# Devuelve múltiples valores desde una función
def obtener_min_max(datos: list[float]) -> tuple[float, float]:
    return min(datos), max(datos)

val_min, val_max = obtener_min_max([12.5, 99.0, 4.2])
```

---

### 4. Diccionarios (`dict`): Tablas Hash Clave-Valor

Los diccionarios constituyen la base directa de los objetos JSON devueltos por FastAPI y las respuestas de APIs RESTful.

```python
# Definición de un registro de telemetría
telemetria_node = {
    "device_id": "MODBUS-092",
    "fase_a_volts": 219.5,
    "fase_b_volts": 221.0,
    "fase_c_volts": 220.2,
    "activo": True
}

# Lectura segura con .get() (evita KeyError)
fase_a = telemetria_node.get("fase_a_volts", 0.0)
fase_d = telemetria_node.get("fase_d_volts", 0.0)  # Retorna 0.0 si no existe

# Modificación e inserción
telemetria_node["fase_a_volts"] = 220.0
telemetria_node["frecuencia_hz"] = 50.0

# Iteración idiomática
for clave, valor in telemetria_node.items():
    print(f"  {clave}: {valor}")
```

---

### 5. Conjuntos (`set`): Colecciones de Elementos Únicos

Los conjuntos implementan tablas Hash para garantizar elementos únicos y realizar operaciones matemáticas de conjuntos de alta velocidad.

```python
sensores_detectados = {"s1", "s2", "s3", "s1", "s2"}
print(sensores_detectados)  # {'s1', 's2', 's3'} (duplicados eliminados)

# Operaciones de Conjuntos
sensores_activos = {"s1", "s2", "s4"}
sensores_mantenimiento = {"s2", "s3"}

# Intersección: Sensores activos que están en mantenimiento
conflicto = sensores_activos & sensores_mantenimiento  # {'s2'}

# Diferencia: Activos operativos limpios
operativos = sensores_activos - sensores_mantenimiento  # {'s1', 's4'}

# Pertenencia ultra rápida O(1)
if "s1" in sensores_activos:
    print("Sensor s1 operando normalmente.")
```

---

### 6. List, Dict y Set Comprehensions

Permiten transformar e filtrar colecciones en una sola línea readable:

```python
lecturas_raw = [10.2, -999.0, 15.8, -999.0, 12.0]

# List Comprehension con filtro
lecturas_ok = [val for val in lecturas_raw if val != -999.0]

# Dict Comprehension
sensores = ["s1", "s2", "s3"]
valores = [42.0, 98.1, 15.0]
mapa_sensores = {s: v for s, v in zip(sensores, valores) if v > 20.0}
# Result: {'s1': 42.0, 's2': 98.1}
```

---

### Resumen de la Lección
Dominar `list`, `tuple`, `dict` y `set` permite manipular cualquier estructura JSON entrante o saliente en endpoints de FastAPI con máxima velocidad y bajo consumo de memoria.
