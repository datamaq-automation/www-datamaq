### 10.1 Conversation-Driven Development and Interactive Learning

El desarrollo guiado por conversaciones (Conversation-Driven Development o CDD) es un proceso iterativo sugerido por Rasa para mejorar progresivamente el asistente basándose en datos de usuarios reales. En lugar de intentar predecir todas las conversaciones desde el inicio, el CDD nos permite descubrir qué realmente dicen los usuarios y ajustar el bot en consecuencia.

#### Objetivos de aprendizaje
- Comprender las seis fases del CDD.
- Aplicar CDD al cotizador de instalaciones eléctricas.
- Usar `rasa interactive` para corregir decisiones del bot en tiempo real.

#### Las 6 fases del CDD aplicadas al cotizador

1. **Share (Compartir)**: entregar el bot preliminar a usuarios reales de prueba lo antes posible. En nuestro caso, podría ser un grupo de clientes potenciales que necesiten cotizar una instalación eléctrica.

2. **Review (Revisar)**: monitorear y leer las transcripciones de las conversaciones reales periódicamente. Buscar mensajes que el bot no entendió o flujos que se rompieron.

3. **Annotate (Anotar/Etiquetar)**: corregir e incorporar los mensajes reales mal clasificados a los datos de entrenamiento NLU. Por ejemplo, si un usuario escribe *"Presupuesto para cablear mi casa"* y el bot clasifica mal la intención, agregamos ese ejemplo a `nlu.yml`.

4. **Test (Probar)**: ejecutar pruebas automatizadas constantes para evitar regresiones. Cada corrección debe ir acompañada de un test que la valide.

5. **Track (Seguir)**: medir la tasa de éxito de las intenciones clave e identificar dónde se producen los abandonos conversacionales. ¿Los usuarios se van durante el formulario? ¿No entienden el estimado?

6. **Fix (Corregir)**: modificar las historias de Core, las validaciones o las respuestas para resolver los cuellos de botella detectados.

#### Aprendizaje interactivo

Mediante el comando `rasa interactive`, podemos conversar con el bot en tiempo real desde la consola. Por cada entrada del usuario, el sistema muestra la intención predicha con su porcentaje de certeza y la siguiente acción del Core, permitiéndonos aprobar o corregir la decisión en caliente. Las correcciones se guardan automáticamente como nuevas historias de entrenamiento.

```bash
rasa interactive
```

#### Ejercicio práctico

1. Invita a dos o tres personas a probar el cotizador con `rasa shell` o desplegado temporalmente.
2. Recopila al menos cinco mensajes que el bot no haya entendido correctamente.
3. Analiza las conversaciones:
   - ¿Qué intenciones fallaron?
   - ¿En qué punto del formulario abandonaron?
   - ¿Qué preguntas hicieron que no están en las FAQs?
4. Incorpora los ejemplos corregidos a `data/nlu.yml` y nuevas historias si es necesario.
5. Ejecuta `rasa interactive` y simula una corrección en vivo.
6. Vuelve a entrenar y ejecuta `rasa test` para verificar que no hay regresiones.

#### Resumen
El CDD transforma las conversaciones reales en combustible para mejorar el bot. En lugar de depender de suposiciones, iteramos sobre datos reales. En el próximo capítulo cerraremos el curso con técnicas de debugging, optimización y recursos de la comunidad Rasa.
