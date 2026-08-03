### Visualización para entender los datos

La visualización es la forma más rápida de detectar patrones, valores atípicos y relaciones. **Matplotlib** es la librería base de gráficos; **Seaborn** la complementa con gráficos estadísticos de alto nivel y estética cuidada.

### Primer gráfico con Matplotlib

```python
import matplotlib.pyplot as plt

horas = list(range(24))
consumos = [30, 28, 27, 29, 31, 35, 48, 62, 71, 68, 60, 55,
            54, 58, 66, 72, 69, 61, 57, 53, 50, 46, 38, 33]

plt.figure(figsize=(10, 5))
plt.plot(horas, consumos, marker="o")
plt.title("Consumo horario de energía")
plt.xlabel("Hora")
plt.ylabel("Potencia (kW)")
plt.grid(True)
plt.show()
```

### Gráficos estadísticos con Seaborn

```python
import seaborn as sns

# Histograma de una variable
sns.histplot(df["potencia_kw"], bins=15)

# Diagrama de caja por categoría
sns.boxplot(data=df, x="zona", y="potencia_kw")

# Relación entre dos variables
sns.scatterplot(data=df, x="consumo_kwh", y="potencia_kw")
```

### Análisis Exploratorio de Datos (EDA)

El **EDA** es el proceso de investigar los datos antes de modelar. Un flujo típico:

```python
# 1. Dimensiones y tipos
print(df.shape)
print(df.dtypes)

# 2. Datos faltantes
print(df.isna().sum())

# 3. Resumen estadístico
print(df.describe())

# 4. Distribución de variables
df.hist(figsize=(10, 8))

# 5. Correlaciones
corr = df.corr()
sns.heatmap(corr, annot=True)
```

### Interpretación de hallazgos

| Hallazgo | Posible acción |
| :--- | :--- |
| Valores atípicos | Investigar su origen antes de eliminar |
| Datos faltantes | Imputar o descartar según el contexto |
| Alta correlación | Seleccionar variables relevantes para el modelo |
| Distribución asimétrica | Considerar transformaciones (log, etc.) |

### Micro-desafío práctico

> Cargá un dataset de tu elección, generá un histograma de una variable numérica y un boxplot por categoría. Documentá con una celda Markdown qué patrones observaste.

### Resumen

- Matplotlib es la base para gráficos de línea, barras e histogramas.
- Seaborn agrega gráficos estadísticos de alto nivel.
- El EDA combina estadísticos, distribución y correlaciones.
- Interpretar los hallazgos orienta las decisiones de limpieza y modelado.
