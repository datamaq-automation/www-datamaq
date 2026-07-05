### 1.5 Introduction to the Rasa Framework

> **Nota importante sobre versionado**
> Este curso se basa en **Rasa Open Source 2.x**. Los conceptos que veremos son válidos para entender el framework, aunque algunos detalles de sintaxis hayan cambiado en Rasa 3.x. Si en el futuro migras a una versión más reciente, la documentación oficial de Rasa tendrá las equivalencias actualizadas.

Rasa es un framework de código abierto en Python diseñado para construir asistentes de inteligencia artificial contextuales y chatbots de nivel empresarial.

#### Ventajas fundamentales

- **Soberanía y seguridad de datos**: puedes desplegar Rasa en tus propios servidores sin enviar los datos conversacionales de tus usuarios a terceros.
- **Personalización completa**: todos los componentes del pipeline pueden configurarse, intercambiarse o escribirse de manera personalizada en Python.
- **Políticas de diálogo avanzadas**: Rasa Core utiliza algoritmos basados en transformadores (como TED) que aprenden de historias reales, en lugar de depender únicamente de árboles lógicos estáticos.

#### Arquitectura básica

- **Rasa Open Source**: incluye el compilador de NLU y el motor de políticas de Core.
- **Rasa SDK**: kit de desarrollo para escribir acciones personalizadas (*Custom Actions*) que ejecutan lógica externa y llamadas a APIs.

#### El proyecto integrador: cotizador de instalaciones eléctricas

A lo largo de este curso construiremos un bot que permita a los usuarios:

1. Solicitar una cotización de instalación eléctrica.
2. Informar el tipo de instalación (residencial, comercial, industrial).
3. Indicar el metraje aproximado.
4. Proporcionar la ubicación.
5. Señalar si la obra es urgente.
6. Recibir un estimado de costo o la opción de agendar una visita técnica.

#### Objetivos de aprendizaje
- Conocer las ventajas de Rasa como framework open-source.
- Entender la arquitectura básica: Rasa Open Source + Rasa SDK.
- Comprender el alcance del bot cotizador que se construirá en el curso.

#### Ejercicio práctico
1. Crea el proyecto base del cotizador:
   ```bash
   rasa init --no-prompt
   mv rasa-bot cotizador-instalaciones-electricas
   cd cotizador-instalaciones-electricas
   ```
2. Explora la estructura generada:
   - `data/nlu.yml`
   - `data/stories.yml`
   - `data/rules.yml`
   - `domain.yml`
   - `config.yml`
   - `endpoints.yml`
   - `credentials.yml`
3. Ejecuta el bot con `rasa shell` y salúdalo.

#### Resumen
Rasa nos permite construir asistentes con control total sobre datos y código. En este curso usaremos Rasa 2.x para desarrollar un cotizador de instalaciones eléctricas. En el próximo capítulo comenzaremos a configurar el NLU para que el bot entienda las primeras intenciones de los usuarios.
