### 4.1 Lógica de negocio con Custom Actions y Formularios

En un asistente conversacional real, la lógica estática de respuestas no es suficiente. Frecuentemente necesitamos conectarnos con sistemas externos, validar reglas complejas o consultar bases de datos.

#### Componentes de Lógica Dinámica en Rasa:
- **Slots**: La memoria del bot. Son variables clave-valor que permiten almacenar información provista por el usuario (extraída de entidades) o cargada externamente (ej. ID de cliente, saldo). Los slots guían el flujo conversacional y modifican las predicciones del modelo si su tipo está configurado para influenciar el diálogo.
- **Custom Actions (Acciones Personalizadas)**: Código Python que se ejecuta en un servidor independiente llamado **Action Server** (comunicándose mediante un webhook HTTP). Permite interactuar con bases de datos, enviar correos o consumir APIs rest.
- **Forms (Formularios)**: Estructuras diseñadas específicamente para recopilar múltiples datos necesarios de forma secuencial. Por ejemplo, para cotizar un servicio necesitamos: nombre, correo, provincia y volumen operativo. El Formulario le pedirá al usuario cada uno de estos datos (slots) que falten y no se detendrá hasta completarlos todos, aplicando validaciones dinámicas en cada paso.
