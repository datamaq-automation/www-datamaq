### 6.1 Consultas a bases de conocimiento en Rasa

Cuando un chatbot necesita interactuar con información detallada de productos, inventarios o servicios que cambian constantemente, escribir respuestas estáticas en el archivo de dominio es ineficiente.

#### Acciones de Base de Conocimiento (Knowledge Base Actions)
Rasa ofrece una integración nativa mediante la clase `ActionQueryKnowledgeBase`. Esto permite que el chatbot responda preguntas contextuales sobre datos estructurados (generalmente provistos en archivos JSON o bases de datos de grafos/relacionales) sin definir cientos de historias redundantes.

#### Casos de Uso Comunes:
- Responder atributos de un objeto: *"¿Qué precio tiene el sensor de energía trifásico?"*.
- Listar objetos filtrados: *"Muéstrame los sensores que sean aptos para intemperie"*.
- Desambiguación y comparación: *"¿Cuál es la diferencia de especificaciones entre el modelo A y el modelo B?"*.

#### Cómo Funciona:
1. El usuario hace una consulta sobre una entidad.
2. El NLU extrae la entidad y el atributo deseado.
3. Rasa ejecuta la acción personalizada que hereda de `ActionQueryKnowledgeBase`.
4. El Action SDK consulta el backend de datos, extrae la información en tiempo real y la formatea dinámicamente como mensaje de respuesta para el usuario.
