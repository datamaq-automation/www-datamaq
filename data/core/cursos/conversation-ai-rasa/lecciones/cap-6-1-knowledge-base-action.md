### 6.1 Knowledge Base Action to Handle Question Answering

Cuando un chatbot necesita interactuar con información detallada de productos, servicios o normativas que cambian con frecuencia, escribir respuestas estáticas en el dominio se vuelve ineficiente. En nuestro cotizador, una base de conocimiento nos permitirá responder preguntas sobre tipos de instalación, materiales y normativas eléctricas sin hardcodear cada respuesta.

#### Objetivos de aprendizaje
- Entender qué es una base de conocimiento y cuándo usarla.
- Crear una base de datos JSON con información del dominio eléctrico.
- Implementar una acción que herede de `ActionQueryKnowledgeBase`.

#### Acciones de base de conocimiento

Rasa ofrece una integración nativa mediante la clase `ActionQueryKnowledgeBase`. Esto permite que el chatbot responda preguntas contextuales sobre datos estructurados sin definir cientos de historias redundantes.

#### Casos de uso en el cotizador eléctrico

- Responder atributos de un objeto: *"¿Cuánto dura una instalación residencial?"*
- Listar objetos filtrados: *"¿Qué tipos de instalación hacen para locales comerciales?"*
- Desambiguación y comparación: *"¿Cuál es la diferencia entre una instalación residencial y una comercial?"*

#### Ejemplo de base de conocimiento

Archivo `data/knowledge_base.json`:
```json
{
  "instalacion": [
    {
      "id": "residencial",
      "nombre": "Instalación residencial",
      "descripcion": "Cableado general para viviendas unifamiliares y departamentos.",
      "tiempo_estimado": "3 a 5 días",
      "garantia_meses": 12
    },
    {
      "id": "comercial",
      "nombre": "Instalación comercial",
      "descripcion": "Cableado para locales, oficinas y comercios con mayor demanda energética.",
      "tiempo_estimado": "5 a 10 días",
      "garantia_meses": 12
    },
    {
      "id": "industrial",
      "nombre": "Instalación industrial",
      "descripcion": "Cableado para plantas, depósitos y grandes superficies con alta tensión.",
      "tiempo_estimado": "10 a 20 días",
      "garantia_meses": 18
    }
  ]
}
```

#### Cómo funciona

1. El usuario hace una consulta sobre una entidad: *"¿Cuánto tarda una instalación comercial?"*
2. El NLU extrae la entidad (`instalacion=comercial`) y el atributo deseado (`tiempo_estimado`).
3. Rasa ejecuta la acción personalizada que hereda de `ActionQueryKnowledgeBase`.
4. El Action SDK consulta el archivo JSON, extrae la información y la formatea como respuesta.

#### Acción personalizada

```python
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase

class ActionMyKB(ActionQueryKnowledgeBase):
    def __init__(self):
        knowledge_base = InMemoryKnowledgeBase("data/knowledge_base.json")
        super().__init__(knowledge_base)
```

#### Ejercicio práctico

1. Crea el archivo `data/knowledge_base.json` con información sobre al menos tres tipos de instalación eléctrica.
2. Implementa una acción personalizada que herede de `ActionQueryKnowledgeBase` y apunte al archivo JSON.
3. Registra la acción en `domain.yml` como `action_query_knowledge_base`.
4. Añade al menos una story o rule que dispare la acción ante la intención `consultar_base_conocimiento`.
5. Entrena el modelo y prueba preguntas como:
   - *"¿Qué es una instalación industrial?"*
   - *"¿Cuánto dura una instalación comercial?"*

#### Resumen
Las acciones de base de conocimiento permiten responder preguntas dinámicas sobre datos estructurados. En nuestro cotizador, esto evita tener que escribir una respuesta estática por cada posible consulta técnica. En el próximo capítulo veremos cómo desambiguar entidades complejas usando roles y grupos.
