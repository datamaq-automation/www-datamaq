### 5.1 Respuestas rápidas y Chitchat con Response Selector

En cualquier chatbot corporativo, existe un gran volumen de preguntas recurrentes (FAQs) como *"¿Cuáles son sus horarios?"*, *"¿Dónde queda su oficina?"* o conversaciones informales (chitchat) como *"¿Cómo estás?"* o *"¿Eres una persona real?"*.

#### El Desafío Tradicional:
Si creamos intenciones e historias de diálogo para cada una de estas preguntas en Rasa Core, nuestro modelo se volverá excesivamente grande y complejo, ralentizando el entrenamiento y aumentando los falsos positivos en las predicciones.

#### La Solución de Rasa: `ResponseSelector`
El `ResponseSelector` es un componente de NLU especializado que procesa preguntas de un solo turno.
- **Intención Raíz**: Agrupamos todas las FAQs bajo una sola intención raíz (por ejemplo, `faq`).
- **Sub-intenciones**: Declaramos sub-intenciones individuales para cada pregunta específica (ej. `faq/horarios`, `faq/ubicacion`).
- **Lógica Simplicada**: Rasa Core solo tiene que aprender a gestionar la intención general `faq` con una única acción de respuesta (`action_utter_faq`).
- **Resolución en NLU**: Internamente, el `ResponseSelector` identifica la sub-intención correspondiente y selecciona la respuesta idónea del dominio, evitando sobrecargar el motor de diálogo conversacional.
