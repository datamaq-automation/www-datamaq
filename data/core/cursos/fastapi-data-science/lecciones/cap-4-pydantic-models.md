### Validación de Datos con Pydantic
Pydantic es la librería que FastAPI utiliza para la serialización y validación de datos. Aprenderemos:

- **Definición de Schemas**: Creación de clases que heredan de `BaseModel` para representar los datos de entrada de los modelos de Machine Learning.
- **Validación Automática**: Cómo FastAPI devuelve automáticamente un error HTTP 422 si los datos del cliente no se ajustan al tipo esperado.
- **Tipos de Datos Avanzados**: Uso de `EmailStr`, `HttpUrl`, listas tipadas y restricciones de rango (por ejemplo, valores numéricos mayores a cero).
- **Configuración de Schemas**: Personalización del comportamiento de serialización mediante la clase `ConfigDict`.
