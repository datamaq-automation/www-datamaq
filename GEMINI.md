# Guía de Desarrollo - Datamaq

## Estándares
- Usar FastAPI con Jinja2 para SSR.
- Todo el contenido debe ir en archivos YAML bajo la carpeta /data.
- Los secretos deben cargarse desde un archivo .env.
- JavaScript debe ser modularizado en /static/js y usar atributos data-* para configuración.
- Seguir lineamientos de AAIERIC.
- **Arquitectura de Bot:** El proyecto servirá como Action Server para RASA (Puerto: 5006).