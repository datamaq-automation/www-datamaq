### La dupla NumPy + Pandas

**NumPy** aporta arrays multidimensionales y operaciones vectoriales de alto rendimiento. **Pandas** se construye sobre NumPy y ofrece estructuras tabulares (Series y DataFrames) pensadas para datos estructurados. Juntas son el núcleo del análisis de datos en Python.

### NumPy: operaciones vectoriales

```python
import numpy as np

# Array unidimensional
consumos = np.array([45.2, 47.1, 46.8, 45.9])

# Operaciones vectorizadas (sin bucles explícitos)
consumos_escala = consumos * 1.1
print(consumos_escala)

# Estadísticas básicas
print(consumos.mean())
print(consumos.max())
print(np.percentile(consumos, 90))
```

### Pandas: Series y DataFrame

La **Series** es una columna etiquetada:

```python
import pandas as pd

s = pd.Series([45.2, 47.1, 46.8], index=["lun", "mar", "mié"])
print(s["mar"])
```

El **DataFrame** es una tabla con filas y columnas:

```python
data = {
    "sensor": ["vfd-01", "vfd-02", "vfd-03"],
    "potencia_kw": [45.2, 32.5, 51.8],
    "zona": ["A", "B", "A"],
}
df = pd.DataFrame(data)
print(df)
```

### Operaciones básicas con DataFrames

```python
# Ver las primeras filas
df.head()

# Resumen estadístico
df.describe()

# Seleccionar una columna
df["potencia_kw"]

# Filtrar filas
df[df["potencia_kw"] > 40]

# Agrupar y agregar
df.groupby("zona")["potencia_kw"].mean()
```

### Carga y guardado de datos

```python
# Leer un CSV
df = pd.read_csv("data/consumo.csv")

# Guardar un CSV procesado
df.to_csv("data/consumo_procesado.csv", index=False)
```

### Ventajas de las operaciones vectoriales

| Enfoque | Ejemplo | Eficiencia |
| :--- | :--- | :--- |
| Bucle Python | `for i in range(len(x))` | Lento en datos grandes |
| Vectorizado NumPy | `x * 1.1` | Mucho más rápido |

### Micro-desafío práctico

> Creá un DataFrame con los consumos diarios de una semana (7 valores). Calculá el promedio, el día de mayor consumo y guardá el resultado en un CSV.

### Resumen

- NumPy permite operaciones vectoriales de alto rendimiento.
- Pandas ofrece Series (columna) y DataFrame (tabla).
- `head()`, `describe()`, filtrado y `groupby` son operaciones esenciales.
- `read_csv` y `to_csv` conectan tus datos con el mundo exterior.
