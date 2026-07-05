### 3.1 Rasa Core

Mientras que Rasa NLU comprende el mensaje actual del usuario, **Rasa Core** decide qué debe hacer el chatbot a continuación. Es el motor de gestión de diálogos y decisiones contextuales. En nuestro cotizador, Core será el encargado de guiar la conversación desde el saludo inicial hasta la entrega del estimado.

#### Objetivos de aprendizaje
- Comprender la diferencia entre stories y rules.
- Configurar las políticas de diálogo en `config.yml`.
- Definir las respuestas iniciales del cotizador en `domain.yml`.

#### Elementos clave en Rasa Core

- **Stories (Historias)**: representan conversaciones reales de ejemplo entre el usuario y el asistente. Se usan para entrenar los modelos de diálogo.  
  Ejemplo para el cotizador:
  ```yaml
  version: "2.0"
  stories:
    - story: cotizacion simple
      steps:
        - intent: saludar
        - action: utter_saludar
        - intent: solicitar_cotizacion
        - action: utter_preguntar_tipo_instalacion
        - intent: informar_tipo_instalacion
        - action: utter_preguntar_metraje
  ```

- **Rules (Reglas)**: fragmentos de conversación que siempre deben seguir el mismo camino, sin importar el contexto previo. Son útiles para saludos, despedidas y respuestas de fallback.  
  Ejemplo:
  ```yaml
  version: "2.0"
  rules:
    - rule: Saludar siempre
      steps:
        - intent: saludar
        - action: utter_saludar

    - rule: Despedirse siempre
      steps:
        - intent: despedirse
        - action: utter_despedirse
  ```

- **Políticas de diálogo (Dialogue Policies)**: algoritmos que determinan la siguiente acción. En `config.yml` podemos declarar varias políticas:
  - `RulePolicy`: evalúa las reglas fijas declaradas.
  - `MemoizationPolicy`: memoriza las historias de entrenamiento y predice si hay coincidencia exacta.
  - `TEDPolicy`: red neuronal transformadora que predice la acción óptima según el contexto histórico, generalizando ante desvíos inesperados.

#### Configuración de policies en `config.yml`

```yaml
policies:
  - name: MemoizationPolicy
  - name: RulePolicy
  - name: TEDPolicy
    max_history: 5
    epochs: 100
```

#### El archivo `domain.yml`

El dominio es el contrato del bot. Debe incluir:

```yaml
version: "2.0"
intents:
  - saludar
  - solicitar_cotizacion
  - informar_tipo_instalacion
  - informar_metraje

responses:
  utter_saludar:
    - text: "¡Hola! Soy el asistente de cotizaciones de instalaciones eléctricas. ¿En qué puedo ayudarte?"
  utter_preguntar_tipo_instalacion:
    - text: "¿Qué tipo de instalación necesitas? ¿Residencial, comercial o industrial?"

session_config:
  session_expiration_time: 60
  carry_over_slots_to_new_session: true
```

#### Ejercicio práctico

1. En tu proyecto `cotizador-instalaciones-electricas`, edita `data/stories.yml` y añade una historia que incluya:
   - Saludo.
   - Solicitud de cotización.
   - Respuesta preguntando el tipo de instalación.
   - Respuesta del usuario indicando el tipo.

2. Edita `data/rules.yml` para agregar reglas de saludo y despedida.

3. Actualiza `domain.yml` con las intenciones, respuestas y acciones necesarias.

4. Entrena el modelo:
   ```bash
   rasa train
   ```

5. Ejecuta el bot en modo conversación:
   ```bash
   rasa shell
   ```

6. Prueba el flujo: saluda, pide una cotización y responde el tipo de instalación.

#### Resumen
Rasa Core decide la siguiente acción del bot usando stories, rules y policies. En esta lección construimos el esqueleto conversacional del cotizador. En el próximo capítulo agregaremos memoria mediante slots y formularios para recopilar toda la información necesaria antes de calcular el estimado.
