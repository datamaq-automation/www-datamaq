### 5.1 Response Selector to Handle Chichat and FAQs

En cualquier chatbot corporativo, existe un gran volumen de preguntas recurrentes (FAQs) como *"¿Cuáles son sus horarios?"*, *"¿Trabajan en mi zona?"* o conversaciones informales (chitchat) como *"¿Cómo estás?"*. Si modelamos cada una de estas preguntas como una intención independiente en Rasa Core, el motor de diálogo se vuelve innecesariamente complejo.

#### Objetivos de aprendizaje
- Entender cuándo usar `ResponseSelector` en lugar de intenciones separadas.
- Configurar sub-intenciones para FAQs del servicio eléctrico.
- Mantener el flujo principal de cotización limpio mientras se responden preguntas puntuales.

#### El desafío tradicional

Si creamos intenciones e historias para cada pregunta frecuente en Rasa Core, el modelo se vuelve excesivamente grande, el entrenamiento se ralentiza y aumentan los falsos positivos. Imagina tener una intención `preguntar_horarios`, otra `preguntar_cobertura`, otra `preguntar_garantía` y todas las historias asociadas.

#### La solución de Rasa: `ResponseSelector`

El `ResponseSelector` es un componente de NLU especializado que procesa preguntas de un solo turno.

- **Intención raíz**: agrupamos todas las FAQs bajo una sola intención raíz, por ejemplo `faq`.
- **Sub-intenciones**: declaramos sub-intenciones individuales para cada pregunta específica: `faq/horarios`, `faq/cobertura`, `faq/garantia`, `faq/tiempos`.
- **Lógica simplificada**: Rasa Core solo aprende a gestionar la intención general `faq` con una única acción de respuesta (`action_utter_faq`).
- **Resolución en NLU**: internamente, el `ResponseSelector` identifica la sub-intención correspondiente y selecciona la respuesta adecuada del dominio.

#### Configuración para el cotizador eléctrico

En `config.yml`:
```yaml
pipeline:
  - name: WhitespaceTokenizer
  - name: RegexFeaturizer
  - name: LexicalSyntacticFeaturizer
  - name: CountVectorsFeaturizer
  - name: DIETClassifier
    epochs: 100
  - name: ResponseSelector
    epochs: 100
```

En `data/nlu.yml`:
```yaml
nlu:
  - intent: faq/horarios
    examples: |
      - ¿Cuáles son los horarios de atención?
      - ¿A qué hora atienden?
      - ¿Están abiertos los sábados?

  - intent: faq/cobertura
    examples: |
      - ¿Trabajan en todas las zonas?
      - ¿Llegan a Córdoba?
      - ¿Atienden en el interior?

  - intent: faq/garantia
    examples: |
      - ¿La instalación tiene garantía?
      - ¿Cuánto dura la garantía?
```

En `domain.yml`:
```yaml
responses:
  utter_faq/horarios:
    - text: "Atendemos de lunes a viernes de 8 a 18 horas."
  utter_faq/cobertura:
    - text: "Trabajamos en todo el país. Dependiendo de la zona, los tiempos de respuesta pueden variar."
  utter_faq/garantia:
    - text: "Todas nuestras instalaciones eléctricas cuentan con garantía de 12 meses."
```

En `data/rules.yml`:
```yaml
rules:
  - rule: Responder FAQ
    steps:
      - intent: faq
      - action: utter_faq
```

#### Chitchat

Para conversaciones informales, se usa el mismo patrón con una intención raíz `chitchat` y sub-intenciones como `chitchat/como_estas`, `chitchat/eres_humano`, `chitchat/gracias`.

#### Ejercicio práctico

1. Añade al menos cinco FAQs del servicio eléctrico en `data/nlu.yml` usando el formato `faq/nombre_de_faq`.
2. Define las respuestas correspondientes en `domain.yml`.
3. Agrega una regla en `data/rules.yml` para responder cualquier FAQ con `utter_faq`.
4. Verifica que el pipeline incluya `ResponseSelector`.
5. Entrena y ejecuta el bot:
   ```bash
   rasa train
   rasa shell
   ```
6. Prueba preguntar por horarios, cobertura y garantía durante una cotización. Observa cómo el bot responde y luego puede continuar el flujo.

#### Resumen
El `ResponseSelector` nos permite manejar FAQs y chitchat de forma elegante, sin saturar el motor de diálogo. En el próximo capítulo veremos cómo conectar el bot con una base de conocimiento para responder preguntas sobre materiales y normativas eléctricas.
