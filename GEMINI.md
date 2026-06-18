# Guía de Desarrollo - Datamaq

## Estándares de Migración (Vue a SSR)
- **Fidelidad UI/UX:** Replicar diseño y transiciones del proyecto legacy.
- **Componentización:** Macros en `templates/partials/macros/`. Cada macro debe ser autocontenido y recibir sus datos por argumentos (evitar contexto global).
- **Comunicación Jinja2 -> JS:** Usar atributos `data-config-*`. Ejemplo: `<div data-config-endpoint="{{ url }}"></div>`.
- **SSR Primario:** El 100% del contenido crítico debe estar en el HTML inicial. JS solo para interactividad y mejoras (Progressive Enhancement).

## Estándares Generales
- **Tecnología:** FastAPI + Jinja2 + YAML.
- **Datos:** Todo el contenido en `/data/*.yaml`.
- **Secretos:** Cargar desde `.env` (no commitear).
- **Bot:** Action Server para RASA en puerto 5006.
