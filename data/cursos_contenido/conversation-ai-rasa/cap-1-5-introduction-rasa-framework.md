### 1.5 Introducción al Framework Rasa

Rasa es un framework de código abierto (open-source) en Python diseñado para construir asistentes de inteligencia artificial contextuales y chatbots de nivel empresarial.

A diferencia de las soluciones en la nube basadas en APIs propietarias (como Google Dialogflow, IBM Watson o Microsoft LUIS), Rasa ofrece ventajas fundamentales:
- **Soberanía y Seguridad de Datos**: Puedes desplegar Rasa en tus propios servidores locales, nubes privadas o nubes públicas sin enviar los datos conversacionales de tus usuarios a terceros.
- **Personalización Completa**: Todos los componentes del pipeline (desde la tokenización hasta el clasificador final de intenciones) pueden configurarse, intercambiarse o escribirse de manera personalizada en Python.
- **Políticas de Diálogo Avanzadas**: Su motor de diálogos (Rasa Core) utiliza algoritmos basados en redes neuronales transformadoras (como TED) que aprenden de flujos reales, en lugar de depender únicamente de árboles lógicos estáticos.

Arquitectura básica:
- **Rasa Open Source**: Incluye el compilador de NLU y el motor de políticas de Core.
- **Rasa SDK**: El kit de desarrollo para escribir acciones personalizadas (*Custom Actions*) que ejecutan lógica externa y llamadas a APIs.
