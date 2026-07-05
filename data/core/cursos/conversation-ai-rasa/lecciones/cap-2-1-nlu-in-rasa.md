### 2.1 Natural Language Understanding in RASA

En el capítulo anterior presentamos las tareas de NLP que Rasa aplica a cada mensaje. En esta lección configuraremos el componente que las ejecuta: **Rasa NLU**. Su trabajo es transformar el texto libre del usuario en una estructura que el diálogo pueda usar: una intención y un conjunto de entidades.

#### Objetivos de aprendizaje
- Definir las intenciones y entidades que necesita nuestro cotizador de instalaciones eléctricas.
- Entender los componentes del pipeline de NLU en `config.yml`.
- Escribir ejemplos de entrenamiento en `data/nlu.yml`.

#### Intenciones del cotizador eléctrico

Una intención representa lo que el usuario quiere hacer. Para nuestro bot, definiremos al menos estas intenciones:

- `solicitar_cotizacion`: el usuario quiere iniciar una cotización.
- `informar_tipo_instalacion`: el usuario indica si es residencial, comercial o industrial.
- `informar_metraje`: el usuario indica los metros cuadrados.
- `informar_ubicacion`: el usuario indica la ciudad o zona.
- `informar_urgencia`: el usuario indica si la obra es normal o urgente.
- `saludar`, `despedirse`, `afirmar`, `negar`: intenciones conversacionales básicas.

#### Entidades del cotizador eléctrico

Las entidades son fragmentos de información estructurada que extraemos del mensaje:

- `tipo_instalacion`: residencial, comercial, industrial.
- `metraje`: número de metros cuadrados.
- `ubicacion`: ciudad, barrio o zona.
- `urgencia`: normal, urgente.
- `nombre`, `telefono`, `email`: datos de contacto.

#### Pipeline de NLU en `config.yml`

El flujo de procesamiento se define secuencialmente y suele incluir:

- **Tokenizers**: dividen la oración en palabras individuales (ej. `WhitespaceTokenizer`).
- **Featurizers**: convierten las palabras en vectores numéricos (ej. `CountVectorsFeaturizer`).
- **Intent Classifiers**: clasifican la intención del mensaje. Rasa utiliza `DIETClassifier`, que realiza clasificación de intenciones y extracción de entidades en una arquitectura unificada.
- **Entity Extractors**: además de `DIETClassifier`, se pueden añadir extractores basados en reglas como `RegexEntityExtractor` o `DucklingEntityExtractor` para números, fechas y medidas.

Ejemplo de configuración mínima para Rasa 2.x:

```yaml
language: es
pipeline:
  - name: WhitespaceTokenizer
  - name: RegexFeaturizer
  - name: LexicalSyntacticFeaturizer
  - name: CountVectorsFeaturizer
  - name: CountVectorsFeaturizer
    analyzer: char_wb
    min_ngram: 1
    max_ngram: 4
  - name: DIETClassifier
    epochs: 100
  - name: EntitySynonymMapper
  - name: ResponseSelector
    epochs: 100
```

#### Ejemplo de `data/nlu.yml`

```yaml
version: "2.0"
nlu:
  - intent: solicitar_cotizacion
    examples: |
      - Quiero cotizar una instalación eléctrica
      - Necesito un presupuesto para cablear una casa
      - ¿Cuánto cuesta una instalación eléctrica comercial?
      - Me interesa una cotización para un local

  - intent: informar_tipo_instalacion
    examples: |
      - Es una instalación [residencial](tipo_instalacion)
      - Es para un local [comercial](tipo_instalacion)
      - Es un depósito [industrial](tipo_instalacion)
```

#### Ejercicio práctico

1. Abre el archivo `data/nlu.yml` del proyecto `cotizador-instalaciones-electricas`.
2. Define las intenciones `informar_metraje`, `informar_ubicacion` e `informar_urgencia` con al menos 5 ejemplos cada una.
3. Asegúrate de etiquetar las entidades en los ejemplos.
4. Entrena el modelo:
   ```bash
   rasa train
   ```
5. Prueba el NLU de forma aislada:
   ```bash
   rasa shell nlu
   ```
6. Escribe mensajes como *"Quiero cotizar para una oficina de 100 metros cuadrados en Buenos Aires"* y verifica que Rasa detecte la intención y las entidades correctamente.

#### Resumen
Rasa NLU nos permite definir qué intenciones y entidades nuestro bot debe reconocer. En esta lección configuramos el pipeline y escribimos los primeros ejemplos de entrenamiento para el cotizador eléctrico. En el próximo capítulo veremos cómo Rasa Core usa esa información para decidir la siguiente acción del diálogo.
