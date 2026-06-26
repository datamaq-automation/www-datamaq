### 9.1 Automatización de tests y despliegue del bot Rasa

Para asegurar que los cambios realizados en el modelo NLU o en las historias no rompan el comportamiento previo del asistente, es indispensable contar con tests automatizados.

#### Historias de Prueba (Test Stories)
En Rasa podemos definir un archivo de pruebas (habitualmente `tests/test_stories.yml`). Estas historias tienen la misma estructura que las historias de entrenamiento, pero se ejecutan mediante el comando `rasa test`.
El sistema simula las entradas del usuario, evalúa la precisión de la clasificación de intenciones y la predicción de acciones del Core, y genera informes con matrices de confusión y métricas F1-Score para ayudarnos a detectar regresiones de calidad.

#### Despliegue en Producción
Para entornos de producción estables, Rasa y su Action Server suelen empaquetarse en contenedores Docker independientes.
- **Docker Compose**: Permite levantar el contenedor de `rasa` (que expone el endpoint HTTP del bot en el puerto 5005) y el contenedor de `rasa-sdk` (que ejecuta el Action Server en el puerto 5055/5006), comunicándolos en una red virtual privada y segura.
- **CI/CD**: Integración con flujos como GitHub Actions para automatizar el reentrenamiento, testing y despliegue del modelo actualizado.
