### 2.2 La Indentación en Python (Indentation Matters)

En la mayoría de los lenguajes de programación (como C, C++, Java o JavaScript), las llaves `{}` o palabras clave delimitadoras (como `begin/end`) determinan los bloques de código. En Python, **la sangría o indentación es parte de la sintaxis del lenguaje** y define la estructura de bloques en funciones, condicionales, bucles y clases.

---

### 1. ¿Por qué la Indentación es Fundamental?

1. **Eliminación de Redundancia**: Evita el uso masivo de llaves `{}` y punto y coma `;`, haciendo que el código sea limpio y sumamente legible.
2. **Standard PEP 8**: La guía de estilo oficial de Python estipula utilizar **4 espacios por nivel de indentación** (se desaconseja el uso de caracteres TAB o mezclar tabulaciones y espacios).
3. **Control de Ámbitos (Scope)**: El nivel de sangría indica qué instrucciones pertenecen a una estructura de control específica.

```python
# Ejemplo Estructurado de Indentación
def verificar_alerta_presion(presion_psi: float) -> str:
    # Inicio de bloque de la función (Nivel 1: 4 espacios)
    if presion_psi > 120.0:
        # Bloque del condicional if (Nivel 2: 8 espacios)
        estado = "CRITICO_VENTEO_REQUERIDO"
    elif presion_psi > 90.0:
        # Bloque del condicional elif (Nivel 2: 8 espacios)
        estado = "ADVERTENCIA_ELEVADO"
    else:
        # Bloque del condicional else (Nivel 2: 8 espacios)
        estado = "NORMAL"
    
    # Retorno al Nivel 1 (4 espacios)
    return estado
```

---

### 2. Errores Comunes de Sangría

#### A. `IndentationError: unexpected indent`
Ocurre al agregar espacios sin haber iniciado un bloque de código (por ejemplo, después de un `:`).

#### B. `IndentationError: expected an indented block`
Ocurre cuando se define un encabezado de función, `if` o `for` que requiere un bloque interno pero no se coloca ninguna línea indentada (se soluciona usando `pass` si el bloque está vacío).

#### C. `TabError: inconsistent use of tabs and spaces in indentation`
Ocurre al mezclar tabulaciones y espacios en un mismo archivo.

---

### 3. Script Práctico: `chapter2_basics_02.py`

Creá el archivo `chapter2_basics_02.py` para verificar cómo la sangría altera el flujo de ejecución y las respuestas de lógica industrial:

```python
"""
Script: chapter2_basics_02.py
Demostración práctica de cómo la indentación afecta el flujo de control y los bloques en Python.
"""

def analizar_eficiencia_linea(vel_linea: float, fallas_detectadas: int) -> dict:
    """
    Analiza métricas de línea de producción respetando bloques por indentación.
    """
    print(f"--> Analizando línea: Velocidad = {vel_linea} m/min | Fallas = {fallas_detectadas}")

    # Bloque 1: Evaluación primaria de velocidad
    if vel_linea > 50.0:
        print("    [Info] Velocidad óptima de producción alcanzada.")
        
        # Bloque 2 anidado: Control de calidad dentro de alta velocidad
        if fallas_detectadas == 0:
            print("    [Éxito] Máxima eficiencia sin fallas.")
            calificacion = "EXCELENTE"
        else:
            print("    [Alerta] Alta velocidad con defectos en piezas.")
            calificacion = "REQUIERE_AJUSTE"
    else:
        print("    [Advertencia] Velocidad por debajo del umbral objetivo.")
        calificacion = "PRODUCCION_BAJA"

    # Este print se ejecuta SIEMPRE al final de la función (está a 4 espacios)
    print(f"--> Calificación final asignada: {calificacion}\n")

    return {
        "velocidad": vel_linea,
        "fallas": fallas_detectadas,
        "calificacion": calificacion
    }

def main():
    print("=" * 60)
    print("📏 DEMOSTRACIÓN: La Indentación en Python (chapter2_basics_02.py)")
    print("=" * 60 + "\n")

    # Caso 1: Alta velocidad sin fallas
    analizar_eficiencia_linea(55.0, 0)

    # Caso 2: Alta velocidad con fallas
    analizar_eficiencia_linea(60.0, 3)

    # Caso 3: Baja velocidad
    analizar_eficiencia_linea(40.0, 0)

if __name__ == "__main__":
    main()
```

#### Ejecución desde la consola:

```bash
python chapter2_basics_02.py
```

*Salida esperada:*
```text
============================================================
📏 DEMOSTRACIÓN: La Indentación en Python (chapter2_basics_02.py)
============================================================

--> Analizando línea: Velocidad = 55.0 m/min | Fallas = 0
    [Info] Velocidad óptima de producción alcanzada.
    [Éxito] Máxima eficiencia sin fallas.
--> Calificación final asignada: EXCELENTE

--> Analizando línea: Velocidad = 60.0 m/min | Fallas = 3
    [Info] Velocidad óptima de producción alcanzada.
    [Alerta] Alta velocidad con defectos en piezas.
--> Calificación final asignada: REQUIERE_AJUSTE

--> Analizando línea: Velocidad = 40.0 m/min | Fallas = 0
    [Advertencia] Velocidad por debajo del umbral objetivo.
--> Calificación final asignada: PRODUCCION_BAJA
```

---

### Resumen de la Lección
La indentación estricta obliga a escribir código estéticamente uniforme y comprensible para todos los miembros del equipo de ingeniería y ciencia de datos. Mantener 4 espacios por nivel es el estándar universal en la comunidad Python.
