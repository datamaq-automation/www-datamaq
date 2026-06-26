### 1.4 Chatbot basics

Un chatbot es una aplicación de software diseñada para simular una conversación con usuarios humanos. No todos los chatbots funcionan igual: la diferencia principal está en cómo deciden qué responder.

#### Tipos de chatbots

1. **Basados en reglas (Rule-based)**: Siguen árboles de decisión rígidos y palabras clave. Son fáciles de crear, pero se rompen ante variaciones en el lenguaje.  
   Ejemplo: si el usuario escribe "presupuesto", responde un mensaje fijo; si escribe "cotización", no entiende.

2. **Basados en IA y contexto (Conversational AI)**: Usan Machine Learning para interpretar el lenguaje natural y mantener el contexto a lo largo de la conversación. Rasa pertenece a esta categoría.  
   Ejemplo: entiende "Quiero cotizar", "Necesito un presupuesto" y "¿Cuánto me sale?" como la misma intención.

3. **Generativos**: Usan grandes modelos de lenguaje (LLMs) para generar respuestas dinámicas. Son muy flexibles pero pueden dar información incorrecta o inventada, lo que es riesgoso en dominios técnicos como instalaciones eléctricas.

#### Componentes esenciales de un asistente conversacional

- **NLU (Natural Language Understanding)**: entiende *qué* dice el usuario.
- **Gestor de diálogo (Dialogue Manager)**: decide *cómo* responder según el historial.
- **Acciones y respuestas (Actions/Responses)**: ejecutan la lógica de negocio y devuelven el mensaje final.

#### Objetivos de aprendizaje
- Distinguir los tres tipos de chatbots.
- Entender por qué Rasa es un chatbot basado en IA y contexto.
- Identificar los tres componentes esenciales de un asistente conversacional.

#### Ejercicio práctico
Clasifica las siguientes interacciones según el tipo de chatbot que las resolvería mejor:

1. El usuario pregunta: *"¿Cuál es el horario de atención?"*
2. El usuario dice: *"Quiero cotizar una instalación eléctrica para mi casa de 120 m2, soy de Rosario y es urgente."*
3. El usuario cambia de tema en medio de una cotización: *"Antes de seguir, ¿cuánto demoran en responder?"*

Justifica por qué un chatbot basado en reglas no sería suficiente para los casos 2 y 3.

#### Resumen
Rasa combina NLU, gestión de diálogo y acciones para crear asistentes que entienden lenguaje natural y mantienen contexto. En la próxima lección conoceremos la arquitectura específica de Rasa y presentaremos formalmente nuestro bot cotizador.
