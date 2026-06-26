### Inyección de Dependencias
La inyección de dependencias es un patrón de diseño que FastAPI implementa de forma nativa mediante la función `Depends`. Permite:

- **Reutilización de Lógica**: Compartir lógica común de autenticación, bases de datos o validación en múltiples endpoints.
- **Modularidad**: Desacoplar la creación de recursos de la lógica de procesamiento del endpoint.
- **Facilidad de Pruebas**: Reemplazar dependencias por stubs o mocks fácilmente durante los tests de integración.
