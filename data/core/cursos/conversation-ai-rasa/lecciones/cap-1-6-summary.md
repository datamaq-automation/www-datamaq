### 1.6 Summary

En este primer módulo sentamos las bases para construir el cotizador de instalaciones eléctricas con Rasa Open Source 2.x.

#### Lo que aprendimos

- Los **requisitos técnicos** para instalar y entrenar Rasa 2.x, incluyendo la versión de Python y la necesidad de un entorno virtual aislado.
- El papel del **Machine Learning** en Rasa: aprender de ejemplos etiquetados para clasificar intenciones y extraer entidades.
- Las tareas de **NLP** que Rasa aplica a cada mensaje: tokenización, featurization, clasificación de intenciones y reconocimiento de entidades.
- Los **tipos de chatbots** y por qué Rasa se ubica en la categoría de IA conversacional basada en contexto.
- La **arquitectura de Rasa**: Rasa Open Source para NLU y Core, y Rasa SDK para acciones personalizadas.
- El **proyecto integrador**: un cotizador de instalaciones eléctricas que recopilará tipo de instalación, metraje, ubicación, urgencia y datos de contacto.

#### Ejercicio práctico
Crea un mapa mental o una lista de chequeo que incluya:

1. Los tres componentes principales de un asistente conversacional en Rasa.
2. Las cuatro tareas de NLP que procesan cada mensaje del usuario.
3. Las cinco piezas de información que debe recopilar nuestro cotizador.
4. La versión de Rasa que usaremos en el curso y por qué es importante recordarlo.

#### Hacia el Módulo 2
En el próximo capítulo entraremos en **Rasa NLU** para definir las intenciones y entidades que nuestro cotizador necesita entender. Comenzaremos escribiendo los primeros ejemplos de entrenamiento en `data/nlu.yml`.
