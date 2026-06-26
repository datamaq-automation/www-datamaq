### 1.2 What is Machine Learning?

El Machine Learning es una rama de la Inteligencia Artificial que permite a las computadoras aprender patrones a partir de datos, sin necesidad de programar reglas explícitas para cada situación. En Rasa, esta idea es central: en lugar de escribir miles de reglas del tipo *"si el usuario dice X, responde Y"*, le damos al modelo ejemplos de lo que los usuarios suelen decir y dejamos que aprenda a generalizar.

#### Conceptos fundamentales aplicados al cotizador eléctrico

- **Datos de entrenamiento**: Son los ejemplos que le mostramos al modelo. En nuestro cotizador de instalaciones eléctricas, un dato de entrenamiento podría ser el mensaje *"Quiero cotizar una instalación eléctrica para mi local comercial"*, etiquetado con la intención `solicitar_cotizacion`.
- **Aprendizaje supervisado**: Le proporcionamos al modelo entradas junto con su salida esperada. Por ejemplo: mensaje → intención, mensaje → entidades extraídas.
- **Entrenamiento (Training)**: Proceso en el que Rasa ajusta los pesos de sus redes neuronales (`DIETClassifier`, `TEDPolicy`) para minimizar los errores de predicción. Se ejecuta con `rasa train`.
- **Inferencia (Inference)**: Una vez entrenado, el modelo recibe mensajes nuevos y predice la intención, las entidades y la siguiente acción del diálogo.

#### Objetivos de aprendizaje
- Comprender qué es el aprendizaje supervisado en Rasa.
- Identificar ejemplos de entrenamiento para el cotizador eléctrico.
- Distinguir entre fase de entrenamiento y fase de inferencia.

#### Ejercicio práctico
Escribe cinco mensajes que un usuario podría enviarle al cotizador de instalaciones eléctricas. Para cada uno, indica:
- ¿Cuál es la intención?
- ¿Qué entidades contiene?

Ejemplo:
- Mensaje: *"Necesito un presupuesto para cablear una oficina de 80 metros cuadrados en Córdoba."*
- Intención: `solicitar_cotizacion`
- Entidades: `tipo_instalacion=comercial`, `metraje=80`, `ubicacion=Córdoba`

#### Resumen
En Rasa, el Machine Learning nos permite entrenar un modelo a partir de ejemplos reales de conversación. En la próxima lección veremos las tareas de Procesamiento del Lenguaje Natural que hacen posible esa comprensión.
