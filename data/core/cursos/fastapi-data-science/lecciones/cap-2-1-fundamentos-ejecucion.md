### 2.1 Fundamentos de Python y Ejecución de Scripts (Basics & Running Scripts)

Python es el lenguaje predilecto para la Ciencia de Datos y el desarrollo de APIs modernas. Para entender cómo frameworks como **FastAPI** aprovechan su potencia, debemos dominar las bases de su arquitectura de ejecución y sus paradigmas.

---

### 1. Lenguaje Interpretado y Bytecode

A diferencia de lenguajes estrictamente compilados a código máquina binario (como C++ o Rust), Python utiliza un modelo híbrido de interpretación eficiente conducido por la máquina virtual estándar **CPython**:

1. **Compilación a Bytecode**: El código fuente escrito en archivos `.py` se compila internamente a un formato de instrucciones intermedias de bajo nivel denominado *bytecode* (almacenado en directorios `__pycache__` como `.pyc`).
2. **Máquina Virtual de Python (PVM)**: La PVM lee secuencialmente las instrucciones de bytecode y las ejecuta sobre la CPU y el sistema operativo.

> **Ventaja en FastAPI**: Este modelo de ejecución dinámica permite la recarga en caliente (*live reload*) en entornos de desarrollo (`uvicorn main:app --reload`), reflejando cambios en el código instantáneamente sin recomplicar la aplicación.

---

### 2. Tipado Dinámico y Fuertemente Tipado

El sistema de tipos de Python destaca por dos pilares conceptuales:

- **Tipado Dinámico (Dynamic Typing)**: Las variables son referencias flexibles o "etiquetas" hacia objetos en memoria. El tipo reside en el objeto en sí, no en la variable.
- **Tipado Fuerte (Strong Typing)**: Python no realiza conversiones implícitas de tipos que puedan derivar en comportamientos ambiguos o pérdida de datos.

```python
# Demostración de Tipado Dinámico
medicion = 100          # 'medicion' referencia a un objeto entero (int)
medicion = "100.5 kW"   # Reasignación a un objeto cadena de texto (str)

# Tipado Fuerte:
# resultado = "Valor: " + 50  --> Eleva TypeError
resultado = "Valor: " + str(50)  # Conversión explícita requerida
```

- **Duck Typing**: *"Si camina como pato y suena como pato, se trata como pato"*. Los objetos son juzgados por sus métodos y atributos disponibles, no por su jerarquía explícita de clases.

---

### 3. Soporte Multiparadigma

Python permite escribir código combinando distintos enfoques de diseño según la complejidad del sistema:

1. **Paradigma Procedural**: Estructuración secuencial basada en funciones y procedimientos directos.
2. **Paradigma Orientado a Objetos (OOP)**: Todo elemento en Python es un objeto. Permite encapsulamiento, herencia y polimorfismo mediante la palabra clave `class`.
3. **Paradigma Funcional**: Las funciones son **ciudadanas de primer orden** (*first-class functions*). Se pueden almacenar en variables, pasar como parámetros y retornar desde otras funciones.

```python
# Ejemplo Funcional: pasaje de funciones como argumentos
def procesar_muestras(datos: list[float], operacion) -> list[float]:
    return [operacion(x) for x in datos]

escalar = lambda v: round(v * 1.8 + 32, 2)  # Conversión C -> F
temperaturas_celsius = [20.0, 25.5, 30.2]

temperaturas_fahrenheit = procesar_muestras(temperaturas_celsius, escalar)
# Resultado: [68.0, 77.9, 86.36]
```

---

### 4. Ejecución de Scripts de Python (`chapter2_basics_01.py`)

Para ejecutar scripts desde la terminal, invoca el binario de `python` seguido del nombre del archivo.

#### El patrón `if __name__ == "__main__":`
Cuando Python ejecuta un script directamente desde la CLI, asigna el valor `"__main__"` a la variable global implícita `__name__`. Si el archivo se importa desde otro script, `__name__` contendrá el nombre del módulo, evitando ejecuciones no deseadas.

Crea el archivo `chapter2_basics_01.py`:

```python
"""
Script: chapter2_basics_01.py
Demostración de ejecución de scripts, tipado dinámico y funciones en Python.
"""
import sys

def calcular_metrica_sensor(nombre: str, lecturas: list[float]) -> dict:
    """Calcula el promedio de lecturas de un sensor industrial."""
    if not lecturas:
        return {"sensor": nombre, "promedio": 0.0, "estado": "SIN_LECTURAS"}
    
    promedio = sum(lecturas) / len(lecturas)
    estado = "OP_NORMAL" if promedio <= 85.0 else "ALERTA_TEMPERATURA"
    
    return {
        "sensor": nombre,
        "promedio": round(promedio, 2),
        "muestras": len(lecturas),
        "estado": estado
    }

def main():
    print("=" * 60)
    print("🚀 EJECUTANDO SCRIPT: chapter2_basics_01.py")
    print(f"🐍 Intérprete Python: {sys.version.split()[0]}")
    print("=" * 60)

    # 1. Variables y tipado dinámico
    datos_telemetria = [45.2, 68.1, 72.4, 89.5]
    print(f"\n[1] Tipo de datos_telemetria: {type(datos_telemetria).__name__}")

    # 2. Invocación de función
    reporte = calcular_metrica_sensor("Sensor_Bomba_Principal", datos_telemetria)
    print(f"[2] Reporte generado: {reporte}")

    # 3. Reasignación dinámica
    datos_telemetria = "Procesamiento finalizado."
    print(f"[3] Reasignado datos_telemetria a: {type(datos_telemetria).__name__}\n")

if __name__ == "__main__":
    main()
```

#### Ejecución desde la consola:

```bash
python chapter2_basics_01.py
```

*Salida esperada:*
```text
============================================================
🚀 EJECUTANDO SCRIPT: chapter2_basics_01.py
🐍 Intérprete Python: 3.10.12 (o superior)
============================================================

[1] Tipo de datos_telemetria: list
[2] Reporte generado: {'sensor': 'Sensor_Bomba_Principal', 'promedio': 68.8, 'muestras': 4, 'estado': 'OP_NORMAL'}
[3] Reasignado datos_telemetria a: str
```
