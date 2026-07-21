### 2.5 Flujo de Control, Bucles y Funciones Dinámicas (*args, **kwargs)

El control de flujo y la modularidad mediante funciones son pilares esenciales para implementar la lógica de negocio de cualquier API web o script de procesamiento de datos.

---

### 1. Control de Flujo Condicional (`if`, `elif`, `else`)

Python permite bifurcar la ejecución del programa evaluando expresiones booleanas:

```python
def categorizar_temperatura(temp_celsius: float) -> str:
    if temp_celsius >= 100.0:
        return "SOBRECALENTAMIENTO_CRITICO"
    elif temp_celsius >= 75.0:
        return "OPERACION_ALTA"
    elif temp_celsius >= 20.0:
        return "OPERACION_NORMAL"
    else:
        return "TEMPERATURA_BAJA"
```

---

### 2. Repetición de Operaciones: Bucles `while` y `for`

#### A. Bucle `while` (Iteración basada en condición)
Ejecuta un bloque de código repetidamente **mientras** una condición booleana sea verdadera. Es ideal cuando el número de iteraciones no se conoce de antemano (ej. reintentos de conexión a una API o base de datos).

```python
import time

def esperar_conexion_db(max_intentos: int = 5) -> bool:
    intento = 1
    conectado = False
    
    # Bucle while: repite mientras no se conecte y queden intentos
    while not conectado and intento <= max_intentos:
        print(f"Intento de conexión #{intento} a la base de datos...")
        # Simulación de verificación
        if intento == 3:
            conectado = True
            print("¡Conexión establecida con éxito!")
        else:
            intento += 1
            
    return conectado
```

#### B. Bucle `for` (Iteración sobre secuencias)
Itera sobre elementos de cualquier secuencia o iterable (listas, tuplas, rangos, diccionarios).

```python
# Iteración sobre un rango numérico
for i in range(1, 4):
    print(f"Procesando lote #{i}")

# Iteración sobre una lista de diccionarios
lecturas = [{"sensor": "s1", "v": 10}, {"sensor": "s2", "v": 20}]
for item in lecturas:
    print(f"Sensor {item['sensor']}: {item['v']} V")
```

---

### 3. Control Fino de Bucles (`break`, `continue` y `else` en bucles)

- **`break`**: Interrumpe inmediatamente la ejecución del bucle actual y sale de él.
- **`continue`**: Salta el resto del código en la iteración actual y pasa inmediatamente a la siguiente iteración.
- **`else` en bucles**: Bloque especial que se ejecuta **únicamente si el bucle terminó de forma natural** (sin haber encontrado un `break`).

```python
def buscar_anomalia_critica(metricas: list[float]) -> float | None:
    for valor in metricas:
        if valor < 0.0:
            print(f"Lectura inválida descartada: {valor}")
            continue  # Salta a la siguiente iteración
            
        if valor > 150.0:
            print(f"🚨 Anomalía crítica encontrada: {valor}")
            return valor  # Rompe la ejecución retornando
            
    else:
        # Se ejecuta SOLO si el bucle terminó sin encontrar valores > 150.0
        print("✅ No se detectaron anomalías críticas en el lote.")
        return None
```

---

### 4. Definición de Funciones

Las funciones en Python se definen con la palabra clave `def`. Permiten encapsular lógica reusable y pueden retornar uno o múltiples valores:

```python
def calcular_eficiencia(potencia_entrada: float, potencia_salida: float) -> tuple[float, str]:
    if potencia_entrada <= 0:
        raise ValueError("La potencia de entrada debe ser mayor a cero.")
        
    eficiencia = (potencia_salida / potencia_entrada) * 100.0
    estado = "OPTIMA" if eficiencia >= 85.0 else "EFICIENCIA_BAJA"
    
    return round(eficiencia, 2), estado

# Invocación y desempaquetado de resultados
porcentaje, estado_op = calcular_eficiencia(100.0, 88.5)
```

---

### 5. Argumentos Dinámicos (`*args` y `**kwargs`)

Cuando una función necesita aceptar un número indeterminado de parámetros posicionales o por clave, Python ofrece la sintaxis de empaquetado `*args` y `**kwargs`.

- **`*args`**: Empaqueta los argumentos posicionales adicionales en una **tupla**.
- **`**kwargs`**: Empaqueta los argumentos nombrados adicionales en un **diccionario**.

```python
def registrar_evento_telemetria(evento: str, *valores_posicionales, **metadatos_extra):
    """
    Función flexible capaz de recibir cualquier cantidad de lecturas y metadatos.
    """
    print(f"📢 Evento: {evento}")
    print(f"📊 Val. Posicionales (*args): {valores_posicionales} | Tipo: {type(valores_posicionales).__name__}")
    print(f"🏷️  Metadatos Extra (**kwargs): {metadatos_extra} | Tipo: {type(metadatos_extra).__name__}\n")

# Invocaciones flexibles:
registrar_evento_telemetria("MEDICION_VOLTAJE", 220.1, 219.8, 220.5)

registrar_evento_telemetria(
    "INSPECCION_PLANTA",
    45.2, 89.1,
    operador="Agustin",
    planta="Avellaneda",
    turno="Mañana"
)
```

---

### Resumen de la Lección
El control de flujo (`if`, `while`, `for`, `break`, `continue`), la declaración clara de funciones y la flexibilidad de `*args` y `**kwargs` constituyen los bloques de construcción necesarios para desarrollar middlewares y controladores robustos en Python y FastAPI.
