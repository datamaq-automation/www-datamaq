### 1.4 Conceptos Básicos de Chatbots

Un chatbot es una aplicación de software diseñada para simular una conversación con usuarios humanos, especialmente a través de internet.

Podemos clasificar los chatbots en tres grandes niveles:
1. **Basados en Reglas (Rule-based)**: Siguen árboles de decisión rígidos y palabras clave específicas. Son sencillos de crear, pero se rompen fácilmente ante variaciones en el texto del usuario.
2. **Basados en IA y Contexto (Conversational AI)**: Utilizan Machine Learning para interpretar el lenguaje natural libre de los usuarios y retener el contexto conversacional a lo largo del tiempo. Rasa pertenece a esta categoría, permitiendo desvíos de flujo naturales.
3. **Generativos**: Utilizan grandes modelos de lenguaje (LLMs) para generar respuestas dinámicas sobre la marcha. Si bien son muy flexibles, requieren controles estrictos para evitar respuestas erróneas o "alucinaciones" en entornos corporativos.

Componentes esenciales de un asistente conversacional moderno:
- **NLU (Natural Language Understanding)**: Entiende *qué* dice el usuario.
- **Gestor de Diálogo (Dialogue Manager)**: Decide *cómo* responder basándose en el historial de la conversación.
- **Acciones y Respuestas (Actions/Responses)**: Ejecutan la lógica de negocio y devuelven el mensaje final.
