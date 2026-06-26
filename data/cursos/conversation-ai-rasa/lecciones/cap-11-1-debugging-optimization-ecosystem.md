### 11.1 Debugging, Optimization, and Community Ecosystem

Cuando un asistente conversacional crece, resolver fallos de clasificación o bucles infinitos en las predicciones requiere herramientas avanzadas de depuración y optimización. En este capítulo final aplicaremos esas técnicas al cotizador de instalaciones eléctricas y revisaremos los recursos disponibles para seguir aprendiendo.

#### Objetivos de aprendizaje
- Depurar el pipeline de NLU y las predicciones del Core.
- Optimizar hiperparámetros clave.
- Conocer los principales recursos de la comunidad Rasa.

#### Técnicas de debugging

- **Consola detallada**: ejecutar los servidores de Rasa con el flag `--debug` expone información pormenorizada del pipeline. Veremos exactamente qué tokens se extrajeron, qué pesos vectoriales se les asignaron y cómo puntuó cada política del Core antes de decidir la acción final.

  ```bash
  rasa shell --debug
  ```

- **Auditoría de acciones**: monitorear las llamadas al Action Server analizando los logs del webhook HTTP permite detectar demoras, excepciones o payloads inválidos. Si el cotizador tarda en entregar el estimado, el primer lugar donde mirar es el log del Action Server.

#### Optimización de hiperparámetros

En el pipeline de `config.yml`, componentes como `DIETClassifier` y `TEDPolicy` cuentan con hiperparámetros ajustables:

- `epochs`: cantidad de iteraciones sobre los datos de entrenamiento. Aumentarlos puede mejorar la precisión, pero un valor excesivo causa *overfitting*.
- `constrain_similar_intents` y `similarity_type`: permiten afinar la separación matemática de intenciones muy similares, como `solicitar_cotizacion` e `informar_tipo_instalacion`.
- `fallback_action_name` y `threshold`: configuran el nivel de confianza mínimo aceptado antes de admitir que el bot no entendió la petición y disparar una acción de disculpa o derivación humana.

#### Ecosistema y comunidad

- **Documentación oficial de Rasa**: aunque este curso usa Rasa 2.x como referencia, la documentación oficial contiene las equivalencias para versiones más recientes.
- **Foro de Rasa**: espacio para resolver dudas específicas y conocer las limitaciones actuales del framework.
- **Repositorio de GitHub**: Rasa Open Source está en modo mantenimiento, pero el código fuente sigue siendo una referencia valiosa.
- **Rasa Pro y CALM**: si en el futuro decides escalar hacia una arquitectura LLM-native, la documentación de Rasa Pro describe el camino de migración.

#### Ejercicio práctico

1. Ejecuta el cotizador en modo debug:
   ```bash
   rasa shell --debug
   ```
2. Envía un mensaje ambiguo como *"Cotizar"* y observa cómo elige la intención.
3. Identifica qué política del Core predice la siguiente acción y con qué confianza.
4. Experimenta con el umbral de fallback en `config.yml`:
   ```yaml
   policies:
     - name: RulePolicy
       core_fallback_threshold: 0.3
       core_fallback_action_name: "action_default_fallback"
   ```
5. Entrena de nuevo y verifica cómo responde el bot ante mensajes de baja confianza.
6. Reflexiona: ¿qué tres aspectos del cotizador mejorarías primero con datos reales?

#### Resumen
En este capítulo final aprendimos a depurar y optimizar el cotizador, y a aprovechar los recursos de la comunidad Rasa. A lo largo del curso construimos un asistente funcional basado en Rasa Open Source 2.x, consciente de que el framework ha evolucionado hacia Rasa Pro y CALM. Los conceptos aprendidos —NLU, Core, slots, forms, custom actions, testing y CDD— siguen siendo la base para construir asistentes conversacionales robustos en cualquier plataforma.
