### 9.1 Testing and Production Deployment

Para asegurar que los cambios realizados en el modelo NLU o en las historias no rompan el comportamiento previo del asistente, es indispensable contar con tests automatizados. Una vez que el cotizador eléctrico funciona correctamente en local, el siguiente paso es empaquetarlo y desplegarlo en un entorno de producción.

#### Objetivos de aprendizaje
- Escribir tests de NLU y tests de Core para el cotizador.
- Interpretar los informes generados por `rasa test`.
- Dockerizar el bot y su Action Server.

#### Historias de prueba (Test Stories)

En Rasa 2.x podemos definir un archivo de pruebas, habitualmente `tests/test_stories.yml`. Estas historias tienen la misma estructura que las historias de entrenamiento, pero se ejecutan mediante el comando `rasa test`.

El sistema simula las entradas del usuario, evalúa la precisión de la clasificación de intenciones y la predicción de acciones del Core, y genera informes con matrices de confusión y métricas F1-Score.

Ejemplo de `tests/test_stories.yml`:
```yaml
version: "2.0"
stories:
  - story: Cotización completa exitosa
    steps:
      - user: |
          Hola
        intent: saludar
      - action: utter_saludar
      - user: |
          Quiero cotizar una instalación eléctrica
        intent: solicitar_cotizacion
      - action: cotizacion_form
      - active_loop: cotizacion_form
      - slot_was_set:
          - tipo_instalacion: residencial
      - slot_was_set:
          - metraje: "80"
      - slot_was_set:
          - ubicacion: Córdoba
      - slot_was_set:
          - urgencia: normal
      - active_loop: null
      - action: action_calcular_estimado
```

#### Tests de NLU

También puedes probar el NLU de forma aislada:
```bash
rasa test nlu
```

Esto genera un informe con la precisión de la clasificación de intenciones y la extracción de entidades.

#### Despliegue en producción

Para entornos estables, Rasa y su Action Server suelen empaquetarse en contenedores Docker independientes.

- **Docker Compose**: permite levantar el contenedor de `rasa` (endpoint HTTP en el puerto 5005) y el contenedor de `rasa-sdk` (Action Server en el puerto 5055), comunicándolos en una red virtual privada.

Ejemplo de `docker-compose.yml`:
```yaml
version: "3.4"
services:
  rasa:
    image: rasa/rasa:2.8.25-full
    ports:
      - 5005:5005
    volumes:
      - ./:/app
    command: run

  action_server:
    image: rasa/rasa-sdk:2.8.2
    ports:
      - 5055:5055
    volumes:
      - ./actions:/app/actions
```

#### CI/CD

Un pipeline básico puede incluir:
1. Instalación de dependencias.
2. Validación de datos: `rasa data validate`.
3. Entrenamiento del modelo: `rasa train`.
4. Ejecución de tests: `rasa test`.
5. Construcción y despliegue de los contenedores.

#### Ejercicio práctico

1. Crea el directorio `tests/` y el archivo `tests/test_stories.yml` con al menos dos historias de prueba del cotizador.
2. Ejecuta los tests:
   ```bash
   rasa test
   ```
3. Revisa el informe generado en `results/`.
4. Crea un `Dockerfile` o `docker-compose.yml` para levantar el bot y el Action Server.
5. Levanta los servicios:
   ```bash
   docker-compose up
   ```
6. Verifica que el bot responde en `http://localhost:5005/webhooks/rest/webhook`.

#### Resumen
Los tests automatizados protegen al cotizador contra regresiones, y Docker permite llevarlo a producción de forma reproducible. En el próximo capítulo veremos cómo seguir mejorando el bot con datos reales de usuarios mediante Conversation-Driven Development.
