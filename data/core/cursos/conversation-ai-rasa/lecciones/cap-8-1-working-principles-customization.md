### 8.1 Working Principles and Customization of Rasa

Una de las grandes ventajas de Rasa Open Source es su modularidad. Si tu aplicación requiere procesar lenguaje de una forma no prevista por los componentes nativos, puedes escribir tus propios componentes en Python. En nuestro cotizador, esto puede ser útil si detectamos que los componentes por defecto no extraen correctamente ciertas expresiones técnicas del dominio eléctrico.

#### Objetivos de aprendizaje
- Comprender el ciclo de vida del entrenamiento en Rasa.
- Conocer los tipos de componentes personalizables.
- Identificar cuándo vale la pena escribir un componente custom en lugar de usar los nativos.

#### Componentes personalizados

Puedes crear:

- **Tokenizers personalizados**: útiles para lenguajes específicos o jergas técnicas donde los tokenizadores estándar fallan al dividir palabras especiales.  
  Ejemplo: expresiones como "100m2", "220V" o "monofásico" podrían requerir un tokenizador que las trate como unidades técnicas.

- **Featurizers personalizados**: para integrar modelos de embedding vectoriales propios o locales.

- **Classifiers personalizados**: para implementar clasificadores de Machine Learning o lógicas de negocio lingüísticas muy específicas.

#### Ciclo de vida del entrenamiento

Cuando ejecutas `rasa train`, Rasa realiza los siguientes pasos:

1. Lee y valida los archivos de datos: `nlu.yml`, `stories.yml`, `rules.yml`.
2. Valida el dominio (`domain.yml`) y detecta inconsistencias.
3. Pasa la información secuencialmente por el pipeline configurado.
4. Entrena los modelos de NLU y Core.
5. Empaqueta los pesos de las redes neuronales y las configuraciones en un archivo comprimido `.tar.gz` dentro del directorio `/models/`.

Este modelo empaquetado es el que Rasa carga al levantar el servidor de producción.

#### ¿Cuándo personalizar?

Antes de escribir un componente custom, conviene agotar las opciones nativas:

1. ¿Ya probaste ajustar el pipeline o agregar más ejemplos de entrenamiento?
2. ¿Los errores son sistemáticos y repetibles en tu dominio?
3. ¿El componente nativo no soporta la estructura lingüística que necesitas?

Si la respuesta es sí en los tres casos, un componente personalizado puede ser la solución.

#### Ejercicio práctico

1. Inspecciona el modelo entrenado:
   ```bash
   ls -la models/
   tar -tzf models/<nombre-del-modelo>.tar.gz | head -20
   ```
2. Identifica qué archivos de configuración y pesos contiene el modelo.
3. En `config.yml`, experimenta cambiando el número de `epochs` del `DIETClassifier` y vuelve a entrenar:
   ```bash
   rasa train
   ```
4. Compara el tamaño del modelo y el tiempo de entrenamiento.
5. Reflexiona: ¿en qué escenario de nuestro cotizador podría ser útil un tokenizer personalizado?

#### Resumen
Rasa permite personalizar casi cualquier componente de su pipeline, pero esa potencia debe usarse con criterio. En esta lección comprendimos el ciclo de entrenamiento y los puntos de extensión del framework. En el próximo capítulo veremos cómo asegurar la calidad del bot mediante tests automatizados y cómo prepararlo para producción.
