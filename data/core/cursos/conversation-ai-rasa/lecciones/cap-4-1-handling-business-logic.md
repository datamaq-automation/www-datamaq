### 4.1 Handling Business Logic

En un asistente conversacional real, la lógica estática de respuestas no es suficiente. Nuestro cotizador necesita recordar lo que el usuario va diciendo, pedir la información que falta y ejecutar un cálculo. Para eso usamos **slots**, **forms** y **custom actions**.

#### Objetivos de aprendizaje
- Usar slots para almacenar información del usuario.
- Crear un formulario que recopile datos de forma secuencial.
- Escribir una custom action que calcule un estimado.
- Conectar Rasa con el Action Server.

#### Componentes de lógica dinámica en Rasa

- **Slots**: son la memoria del bot. Son variables clave-valor que almacenan información proporcionada por el usuario o cargada externamente. En nuestro cotizador usaremos slots para guardar `tipo_instalacion`, `metraje`, `ubicacion` y `urgencia`.

  ```yaml
  slots:
    tipo_instalacion:
      type: text
      influence_conversation: true
    metraje:
      type: text
      influence_conversation: false
    ubicacion:
      type: text
      influence_conversation: false
    urgencia:
      type: categorical
      values:
        - normal
        - urgente
      influence_conversation: true
  ```

- **Forms (Formularios)**: estructuras diseñadas para recopilar múltiples datos necesarios de forma secuencial. El formulario le pedirá al usuario cada slot que falte y no se detendrá hasta completarlos todos.

  ```yaml
  forms:
    cotizacion_form:
      required_slots:
        - tipo_instalacion
        - metraje
        - ubicacion
        - urgencia
  ```

- **Custom Actions**: código Python que se ejecuta en un servidor independiente llamado **Action Server** (comunicándose mediante un webhook HTTP). Permiten interactuar con bases de datos, enviar correos o, en nuestro caso, calcular un estimado.

  ```python
  from typing import Any, Text, Dict, List
  from rasa_sdk import Action, Tracker
  from rasa_sdk.executor import CollectingDispatcher

  class ActionCalcularEstimado(Action):
      def name(self) -> Text:
          return "action_calcular_estimado"

      def run(self, dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

          tipo = tracker.get_slot("tipo_instalacion")
          metraje = tracker.get_slot("metraje")
          ubicacion = tracker.get_slot("ubicacion")
          urgencia = tracker.get_slot("urgencia")

          # Fórmula de ejemplo para Rasa 2.x
          precio_por_m2 = {"residencial": 1500, "comercial": 2200, "industrial": 3000}
          base = precio_por_m2.get(tipo, 1500) * int(metraje)
          if urgencia == "urgente":
              base *= 1.3

          dispatcher.utter_message(
              text=f"El estimado para una instalación {tipo} de {metraje} m² en {ubicacion} es de ${base:,.0f}."
          )
          return []
  ```

#### Ejercicio práctico

1. En `domain.yml`, define los slots `tipo_instalacion`, `metraje`, `ubicacion` y `urgencia`, y el formulario `cotizacion_form`.
2. Crea una story que active el formulario:
   ```yaml
   stories:
     - story: cotizacion con formulario
       steps:
         - intent: solicitar_cotizacion
         - action: cotizacion_form
         - active_loop: cotizacion_form
         - active_loop: null
         - action: action_calcular_estimado
   ```
3. Implementa la custom action `action_calcular_estimado` en `actions/actions.py`.
4. Configura `endpoints.yml` para apuntar al Action Server:
   ```yaml
   action_endpoint:
     url: "http://localhost:5055/webhook"
   ```
5. En una terminal, levanta el Action Server:
   ```bash
   rasa run actions
   ```
6. En otra terminal, entrena y ejecuta el bot:
   ```bash
   rasa train
   rasa shell
   ```
7. Solicita una cotización y completa todos los campos que te pida el formulario.

#### Resumen
Los slots permiten recordar información, los forms la recopilan de forma estructurada y las custom actions ejecutan la lógica de negocio. En esta lección nuestro cotizador ya puede entregar un estimado. En el próximo capítulo aprenderemos a manejar preguntas frecuentes y conversaciones informales sin que interfieran con el flujo principal.
