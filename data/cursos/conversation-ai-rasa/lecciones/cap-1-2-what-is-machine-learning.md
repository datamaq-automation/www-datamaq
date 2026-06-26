### 1.2 ¿Qué es el Aprendizaje Automático (Machine Learning)?

El Aprendizaje Automático es una rama de la Inteligencia Artificial que permite a las computadoras aprender y mejorar a partir de la experiencia (datos) sin ser programadas explícitamente para cada tarea.

Conceptos fundamentales:
- **Datos de entrenamiento**: Conjunto de ejemplos que el modelo procesa para identificar patrones y relaciones. En Rasa, estos datos consisten en intenciones (mensajes de ejemplo) e historias de conversación.
- **Aprendizaje Supervisado**: El tipo de aprendizaje que utiliza Rasa. Le proporcionamos ejemplos de entrada etiquetados con su salida correcta (por ejemplo, el mensaje *"hola"* etiquetado con la intención `saludo`).
- **Entrenamiento (Training)**: El proceso mediante el cual los algoritmos ajustan sus parámetros internos para minimizar el error de predicción en base a los datos suministrados.
- **Inferencia (Inference)**: Fase en la que el modelo ya entrenado recibe nuevos datos no vistos previamente y realiza una predicción (por ejemplo, clasificar un mensaje desconocido bajo una intención específica).
