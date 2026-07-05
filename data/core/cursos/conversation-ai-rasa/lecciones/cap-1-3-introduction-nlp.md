### 1.3 Introduction to Natural Language Processing (NLP)

El Procesamiento del Lenguaje Natural (NLP) combina lingüística computacional y modelado estadístico para permitir que las máquinas procesen, entiendan y generen lenguaje humano de manera útil. En Rasa, el NLP no es un tema abstracto: es el conjunto de operaciones que transforma el mensaje del usuario en decisiones concretas para el cotizador eléctrico.

#### Tareas clave de NLP en nuestro cotizador

- **Tokenización**: Dividir el texto en unidades más pequeñas llamadas *tokens*.  
  Ejemplo: *"Quiero cotizar una instalación residencial"* → `["Quiero", "cotizar", "una", "instalación", "residencial"]`
- **Extracción de características (Featurization)**: Convertir los tokens en vectores numéricos que los algoritmos de Machine Learning puedan procesar. Rasa usa representaciones densas y dispersas según el componente del pipeline.
- **Reconocimiento de Entidades Nombradas (NER)**: Identificar información estructurada en el texto libre.  
  Ejemplo: en *"Necesito cotizar para un depósito de 500 m2"*, extraemos `tipo_instalacion=industrial` y `metraje=500`.
- **Clasificación de Intenciones**: Determinar la intención del mensaje.  
  Ejemplo: *"¿Cuánto cuesta una instalación?"* → intención `solicitar_cotizacion`.

#### Objetivos de aprendizaje
- Entender las cuatro tareas de NLP que Rasa aplica a cada mensaje.
- Reconocer tokens, intenciones y entidades en mensajes del cotizador.
- Comprender por qué el pipeline de NLU es configurable.

#### Ejercicio práctico
Analiza el siguiente mensaje como lo haría Rasa:

> *"Hola, necesito un presupuesto para cablear un local comercial de 120 metros cuadrados. Es urgente."*

Responde:
1. ¿Cuáles son los tokens?
2. ¿Cuál es la intención probable?
3. ¿Qué entidades y valores detectas?
4. ¿Qué información aún falta para poder cotizar?

#### Resumen
El pipeline de NLP de Rasa convierte el lenguaje libre del usuario en una estructura que el diálogo puede usar: intenciones, entidades y características numéricas. En el próximo capítulo aprenderemos a configurar ese pipeline para el cotizador eléctrico.
