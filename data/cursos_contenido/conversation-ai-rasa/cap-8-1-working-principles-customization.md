### 8.1 Personalización y desarrollo de componentes customizados en Rasa

Una de las grandes ventajas competitivas de Rasa Open Source es su modularidad. Si tu aplicación requiere procesar lenguaje de una forma no prevista por los componentes nativos, puedes escribir tus propios componentes en Python.

#### Componentes Personalizados (Custom Components)
Puedes crear:
- **Tokenizers personalizados**: Útiles para lenguajes específicos o jergas técnicas donde los tokenizadores estándar fallan al dividir palabras especiales.
- **Featurizers personalizados**: Para integrar modelos de embedding vectoriales propios o locales.
- **Classifiers personalizados**: Para implementar clasificadores de Machine Learning o lógicas de negocio lingüísticas muy específicas.

#### Ciclo de Vida del Entrenamiento
Cuando ejecutas `rasa train`, Rasa compila todos los archivos de datos (`nlu.yml`, `stories.yml`, `rules.yml`), valida el dominio (`domain.yml`) y pasa la información secuencialmente por el pipeline configurado. Al finalizar, empaqueta los pesos de las redes neuronales y las configuraciones entrenadas en un archivo comprimido `.tar.gz` dentro del directorio `/models/`. Este modelo empaquetado es el que Rasa carga al levantar el servidor de producción.
