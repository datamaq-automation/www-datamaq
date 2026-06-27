# Lista de Tareas Pendientes (TODO.md)

Este documento centraliza las tareas de mantenimiento, documentación y optimización para el proyecto **www-datamaq**.

---

## Tareas de Optimización y SEO (# P2)
- [x] Cambiar la jerarquía de encabezados en [instructor.html](file:///home/agustin/proyectos_software/www-datamaq/templates/cursos/instructor.html#L34-L38) para que el tag H1 contenga el nombre del instructor en lugar de un título de sección genérico. # P2
- [x] Robustecer el helper `canonical_url` en [seo.py](file:///home/agustin/proyectos_software/www-datamaq/src/infrastructure/fastapi/utils/seo.py#L5) utilizando una constante `BASE_URL` en lugar de `request.url` dinámico, previniendo canonicals erróneos si el proxy está mal configurado. # P2
- [x] Mejorar los textos descriptivos alternativos (`alt`) genéricos de las fotos de los técnicos en [contenido.yaml](file:///home/agustin/proyectos_software/www-datamaq/data/contenido.yaml#L9). # P2
- [ ] Modificar [hero.html](file:///home/agustin/proyectos_software/www-datamaq/templates/partials/components/hero.html#L11) para renderizar el botón de acción secundario configurado en el archivo YAML de contenido. # P2
- [ ] Implementar la inyección dinámica de datos estructurados Schema.org para `FAQPage` y `Person` en los templates correspondientes. # P2
