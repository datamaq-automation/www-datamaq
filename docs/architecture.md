# Arquitectura del Sistema - Datamaq

## Diagrama Lógico
1. **Capa de Configuración:** Carga de variables de entorno (.env).
2. **Capa de Datos:** Carga de archivos YAML desde /data.
3. **Capa de Aplicación (FastAPI):** Inyección de datos, lógica de negocio y endpoint para RASA Action Server (puerto 5006).
4. **Capa de Presentación (Jinja2):** Renderizado final de HTML.
5. **Capa de Comportamiento (Frontend JS):** Inicialización de componentes (Chat) mediante lectura de atributos data-*.

## Calidad y Testing
- Se utiliza *pytest* para la suite de pruebas unitarias e integración.
- La cobertura se mantiene por encima del 90% (verificado con *pytest-cov*).
- Se ha implementado un *pre-push hook* (en *scripts/pre-push.sh*) que automatiza la ejecución de pruebas antes de cualquier envío al repositorio.

## Optimización
- Los activos estáticos utilizan cabeceras Cache-Control (7 días).

## Despliegue Continuo (CD)
- El despliegue está automatizado mediante GitHub Actions al hacer push a la rama `main`.
- El flujo utiliza `scripts/deploy-server.sh` en el VPS para actualizar código, dependencias, aplicar *cache busting* y reiniciar el servicio `systemd`.
- Requiere los siguientes secretos configurados en GitHub: `SSH_HOST`, `SSH_PRIVATE_KEY`.
