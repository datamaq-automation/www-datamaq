### 11.1 Depuración y optimización de asistentes en Rasa

Cuando un asistente conversacional crece, resolver fallos de clasificación o bucles infinitos en las predicciones requiere herramientas avanzadas de depuración y optimización.

#### Técnicas de Debugging:
- **Consola Detallada**: Ejecutar los servidores de Rasa con el flag `--debug` expone información pormenorizada del pipeline. Veremos exactamente qué tokens se extrajeron, qué pesos vectoriales se les asignaron y cómo puntuó cada política del Core antes de decidir la acción final.
- **Auditoría de Acciones**: Monitorear las llamadas al Action Server analizando los logs del webhook HTTP para detectar demoras, excepciones o payloads inválidos.

#### Optimización de Hiperparámetros:
En el pipeline de `config.yml`, componentes como `DIETClassifier` y `TEDPolicy` cuentan con hiperparámetros ajustables:
- `epochs`: Cantidad de iteraciones sobre los datos de entrenamiento (por defecto 100). Aumentarlos puede mejorar la precisión, pero un valor excesivo causa *overfitting* (sobreajuste).
- `constrain_similar_intentities` y `similarity_type`: Permiten afinar la separación matemática de intenciones muy similares.
- `fallback_action_name` y `threshold`: Configuraciones del fallback que deciden el nivel de confianza mínimo aceptado (ej. 0.6) antes de admitir que el bot no entendió la petición y disparar una acción de disculpa o derivación.
