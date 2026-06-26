### 7.1 Roles y grupos de entidades en Rasa NLU

En flujos conversacionales de complejidad media y avanzada, no basta con identificar que una palabra pertenece a un tipo de entidad genérico. Necesitamos capturar el contexto gramatical o agrupamiento en el que se encuentra.

Para resolver este desafío, Rasa introduce:
- **Roles de Entidad (Entity Roles)**: Permiten etiquetar una misma entidad con diferentes funciones dentro de un mensaje.
  * Ejemplo: *"Quiero viajar de **Rosario** a **Córdoba**"*.
  * Aquí, tanto *"Rosario"* como *"Córdoba"* son entidades tipo `localidad`.
  * Definimos el rol `origen` para *"Rosario"* y el rol `destino` para *"Córdoba"*.
- **Grupos de Entidades (Entity Groups)**: Permiten asociar entidades relacionadas que pertenecen al mismo concepto dentro de una frase.
  * Ejemplo: *"Quiero comprar una **campera azul talle L** y una **remera roja talle M**"*.
  * Necesitamos asociar el color `azul` y el talle `L` específicamente al producto `campera`, y el color `roja` y talle `M` a `remera`.
  * Definimos grupos separados para evitar que los datos se mezclen en la base de datos o en la acción personalizada.

Ambas configuraciones se entrenan en el dataset NLU y son procesadas nativamente por el extractor `DIETClassifier`.
