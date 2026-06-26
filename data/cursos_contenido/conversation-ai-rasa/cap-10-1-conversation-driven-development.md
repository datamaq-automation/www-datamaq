### 10.1 CDD (Conversation-Driven Development) y Aprendizaje Interactivo

El desarrollo guiado por conversaciones (Conversation-Driven Development o CDD) es un proceso iterativo sugerido por Rasa para mejorar progresivamente tu asistente basándote en datos de usuarios reales.

#### Las 6 fases del CDD:
1. **Share (Compartir)**: Entregar el bot preliminar a usuarios reales de prueba lo antes posible.
2. **Review (Revisar)**: Monitorear y leer las transcripciones de las conversaciones reales periódicamente.
3. **Annotate (Anotar/Etiquetar)**: Corregir e incorporar los mensajes reales mal clasificados a los datos de entrenamiento NLU.
4. **Test (Probar)**: Ejecutar pruebas automatizadas constantes para evitar regresiones.
5. **Track (Seguir)**: Medir la tasa de éxito de las intenciones clave e identificar dónde se producen los abandonos conversacionales.
6. **Fix (Corregir)**: Modificar las historias de Core o las validaciones para resolver los cuellos de botella detectados.

#### Aprendizaje Interactivo (Interactive Learning)
Mediante el comando `rasa interactive`, podemos conversar con el bot en tiempo real desde la consola. Por cada entrada del usuario, el sistema nos muestra la intención predicha con su porcentaje de certeza y la siguiente acción del Core, permitiéndonos aprobar o corregir la decisión en caliente, guardando automáticamente las correcciones como nuevas historias de entrenamiento.
