### 2.1 Comprensión del Lenguaje Natural con Rasa NLU

Rasa NLU es el componente encargado del procesamiento del lenguaje para extraer el significado de los mensajes del usuario. Su objetivo principal es resolver dos problemas:
1. **Intents (Intenciones)**: Clasificar qué es lo que el usuario quiere hacer o decir.
2. **Entities (Entidades)**: Extraer variables u objetos estructurados del texto (ej. números, fechas, nombres).

#### Pipeline de NLU en `config.yml`
El flujo de procesamiento se define secuencialmente y suele incluir:
- **Tokenizers**: Dividen la oración en palabras individuales (ej. `WhitespaceTokenizer`, `SpacyTokenizer`).
- **Featurizers**: Convierten las palabras en representaciones vectoriales densas o dispersas (ej. `CountVectorsFeaturizer`, `LanguageModelFeaturizer`).
- **Intent Classifiers**: Clasifican la intención del mensaje completo. Rasa utiliza `DIETClassifier` (Dual Intent and Entity Transformer) por defecto, el cual realiza clasificación de intenciones y extracción de entidades en una arquitectura unificada de transformadores.
- **Entity Extractors**: Extraen información específica. Además de `DIETClassifier`, se pueden añadir extractores basados en reglas como `RegexEntityExtractor` (para patrones fijos) o `DucklingEntityExtractor` (para números, fechas y medidas).
