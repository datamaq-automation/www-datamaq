# Historial de Tareas Completadas (TODO.done.md)

Este documento registra todas las tareas de mantenimiento, documentación y optimización del proyecto **www-datamaq** que ya han sido implementadas con éxito.

---

## Tareas Completadas

### Tareas Críticas e Infraestructura (# P0)
- [x] Corregir la directiva de robots en [head.html](file:///home/agustin/proyectos_software/www-datamaq/templates/partials/head.html#L38) para que reconozca el valor dinámico `seo_data.meta_robots` provisto por el backend (evita indexación no deseada de las lecciones). # P0
- [x] Corregir el middleware canónico en [middleware.py](file:///home/agustin/proyectos_software/www-datamaq/src/infrastructure/fastapi/middleware.py#L58) para conservar los query parameters (UTM tracking) en las redirecciones de normalización de URL. # P0

### Tareas de Documentación y Normativa (# P1)
- [x] Crear el documento `docs/cursos.md` con la guía práctica para redactar y dar de alta nuevas lecciones técnicas y registrar los cursos en el archivo `curso.yaml`. # P1
- [x] Inicializar el archivo de bitácora `docs/DISCOVERY.md` para estructurar dudas y ambigüedades técnicas que los agentes encuentren en el proyecto. # P1
- [x] Crear el archivo `static/manifest.json` y referenciarlo en [head.html](file:///home/agustin/proyectos_software/www-datamaq/templates/partials/head.html) para proveer metadata de PWA básica y mejorar el SEO móvil. # P1
- [x] Agregar las URLs de perfiles de instructores al sitemap dinámico generado en [main_routes.py](file:///home/agustin/proyectos_software/www-datamaq/src/infrastructure/fastapi/routes/main_routes.py#L53). # P1

### Tareas de Optimización y SEO (# P2)
- [x] Analizar si es conveniente retirar la etiqueta `noindex` de las lecciones e incorporarlas en el sitemap dinámico para captar tráfico orgánico de búsquedas técnicas (Se resolvió estratégicamente mantener el noindex para priorizar leads B2B y evitar ruido comercial). # P2
- [x] Cambiar la jerarquía de encabezados en [instructor.html](file:///home/agustin/proyectos_software/www-datamaq/templates/cursos/instructor.html#L34-L38) para que el tag H1 contenga el nombre del instructor en lugar de un título de sección genérico. # P2
- [x] Robustecer el helper `canonical_url` en [seo.py](file:///home/agustin/proyectos_software/www-datamaq/src/infrastructure/fastapi/utils/seo.py#L5) utilizando una constante `BASE_URL` en lugar de `request.url` dinámico, previniendo canonicals erróneos si el proxy está mal configurado. # P2
- [x] Mejorar los textos descriptivos alternativos (`alt`) genéricos de las fotos de los técnicos en [contenido.yaml](file:///home/agustin/proyectos_software/www-datamaq/data/contenido.yaml#L9). # P2
- [x] Modificar [hero.html](file:///home/agustin/proyectos_software/www-datamaq/templates/partials/components/hero.html#L11) para renderizar el botón de acción secundario configurado en el archivo YAML de contenido. # P2
- [x] Implementar la inyección dinámica de datos estructurados Schema.org para `FAQPage` y `Person` en los templates correspondientes. # P2
