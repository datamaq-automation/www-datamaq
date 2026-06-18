# Arquitectura del Sistema - Datamaq

## Flujo de Datos y Componentización
Para replicar la modularidad de Vue en un entorno SSR:

1.  **Capa de Datos:** Archivos YAML inyectados en el contexto de FastAPI.
2.  **Capa de Presentación (Macros):** 
    - Ubicación: `src/infrastructure/fastapi/templates/partials/macros/`.
    - Patrón: `{{ macro_name(data) }}`.
3.  **Capa de Comportamiento (JS):** 
    - Los componentes de JS en `static/js/` se inicializan buscando elementos con atributos `data-component-name`.
    - La configuración se extrae de atributos `data-config-*`.

## Integración RASA
- El proyecto actúa como **Action Server**.
- Endpoint: `/webhook`.
- Puerto: 5006.

## Infraestructura y CD
- Despliegue automático vía GitHub Actions.
- Script de despliegue: `scripts/deploy-server.sh`.
