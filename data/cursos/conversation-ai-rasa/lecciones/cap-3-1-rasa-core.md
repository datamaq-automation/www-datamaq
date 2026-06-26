### 3.1 Gestión de flujos de diálogo con Rasa Core

Mientras que Rasa NLU se encarga de comprender el mensaje actual del usuario, Rasa Core decide qué debe hacer el chatbot a continuación. Es el motor de gestión de diálogos y decisiones contextuales.

#### Elementos Clave en Rasa Core:
- **Stories (Historias)**: Representan conversaciones reales de ejemplo entre un usuario y el asistente. Se estructuran en formato YAML y sirven para entrenar los modelos de machine learning del motor de diálogos.
- **Rules (Reglas)**: Fragmentos de conversación que siempre deben seguir el mismo camino, sin importar el contexto previo (por ejemplo, responder a un saludo o a un insulto).
- **Políticas de Diálogo (Dialogue Policies)**: Algoritmos que determinan la acción siguiente. En `config.yml` podemos declarar varias políticas:
  - `RulePolicy`: Evalúa las reglas fijas declaradas.
  - `MemoizationPolicy`: Memoriza las historias del archivo de entrenamiento y predice la acción si hay una coincidencia exacta de historial.
  - `TEDPolicy` (Transformer Embedding Dialogue Policy): Una red neuronal de tipo transformador que predice la acción óptima en base al contexto histórico, siendo capaz de generalizar y manejar desvíos inesperados en la conversación.
