# Resumen Ejecutivo — Optimización SEO de bajo nivel

**Rama:** `feature/seo-optimizacion`  
**Fecha:** 2026-07-05  
**Estado:** Listo para review.

---

## 1. Qué se mejoró

### A. Archivos de descubrimiento
1. **Creación de `static/humans.txt`** con información del equipo, ubicación y stack tecnológico.
2. **Exposición de `/humans.txt`** mediante un endpoint en `src/infrastructure/fastapi/routes/main_routes.py` que sirve el archivo con `media_type="text/plain"`.
3. **Configuración centralizada** de la ruta del archivo en `src/infrastructure/settings/config.py` (`HUMANS_TXT_PATH`).

### B. Datos estructurados (JSON-LD)
4. **`/contact`** ahora inyecta un bloque JSON-LD de tipo `ContactPage` con la organización como `mainEntity`, mejorando la semántica de la página de contacto.
5. **`/cursos/instructor/{instructor_id}`** ahora incluye un `BreadcrumbList` (Inicio → Cursos → Instructor), alineándose con el resto de las páginas de detalle.

### C. Optimización de imágenes
6. Se agregó `decoding="async"` a las imágenes de cursos, instructores y tarjetas de curso para reducir el trabajo en el hilo principal.
7. Se agregó `loading="lazy"` a las fotos de instructor dentro de las tarjetas de curso y en la página de perfil del instructor.
8. Se mantuvo `fetchpriority="high"` y `loading="eager"` en la imagen hero de la Home, que está en el viewport inicial.

### D. Sitemap dinámico
9. El `lastmod` del sitemap ahora se calcula a partir de la fecha de modificación más reciente de los archivos de datos (`data/**/*.yaml`, `data/**/*.md`) en lugar de usar la fecha actual en cada request.
10. El sitemap sigue exponiendo URLs canónicas absolutas (`https://datamaq.com.ar/...`) para Home, contacto, términos, cursos, localidades, industrias e instructores.

### E. Redirecciones y manejo de 404
11. Se eliminó el **wildcard 301 de 404 a `/`** en `src/infrastructure/fastapi/app.py`. Ahora cualquier URL desconocida devuelve una respuesta 404 real con la plantilla `404.html` (`noindex, follow`).
12. Se creó **`data/redirects.yaml`** para configurar redirecciones 301 puntuales hacia URLs legacy de la SPA anterior sin tocar código.
13. `DataService` expone `get_redirects()` para leer y cachear el archivo de redirecciones.

### F. Modelado de asistencia técnica híbrida (campo + remota)
14. Se agregó `assistance_modes` en `data/contenido.yaml` con `on_site` (visitas en campo) y `remote` (asistencia remota/consultoría).
15. Se agregó el campo `modality` a cada tarjeta de servicio (`on_site`, `remote`, `both`) y se muestra en las tarjetas de servicio de la Home.
16. Se agregó una **sección de modalidades** en la Home (`templates/index.html`) que presenta ambas formas de asistencia técnica.
17. Se extendió `FieldModel` en `src/domain/models.py` para soportar campos de tipo `select` con opciones.
18. Se agregó al formulario de contacto un select de **modalidad de asistencia preferida** (campo, remoto, ambas), modelado desde `data/contenido.yaml`.

### G. Alineación del copy con el negocio principal
19. Se reescribió el **hero de la Home** para comunicar "asistencia técnica híbrida" (campo + remota) como mensaje principal, mencionando las capacitaciones de cortesía como complemento.
20. Se ajustaron los títulos y descripciones de las tarjetas de servicio:
    - "Instalación de equipos IoT en campo" (visitas técnicas).
    - "Asesoramiento técnico remoto" (consultoría a distancia).
    - "Capacitaciones técnicas de cortesía" (formación gratuita, no producto principal).

### H. Calidad y cobertura
21. Se validó que `pytest` continúa pasando al 100% (41 tests).
22. Se validó que `mypy` sigue limpio sobre `src/`.
23. No se redujo la cobertura de tests ni se modificó la arquitectura de capas.

---

## 2. Qué quedó documentado en `docs/DUDAS.md`

Las siguientes decisiones estratégicas o de alto impacto no se implementaron de forma autónoma y quedaron pendientes de consulta:

- **Indexación de lecciones individuales**: mantener `noindex` o indexar contenido educativo long-tail.
- **Arquitectura de CSS y purga de Tailwind**: medir bloat, purgar clases no usadas y reorganizar `static/css/`.
- **CSS crítico inline** para Above The Fold de la Home y rutas críticas.
- **Expansión de landings geográficas e industriales**: qué localidades/sectores agregar con contenido diferenciado.
- **Completar mapeo de URLs legacy** en `data/redirects.yaml` a partir de logs o Search Console.
- **Estrategia de contenido** (blog, casos de éxito, guías técnicas) para autoridad de dominio.
- **Dimensiones explícitas** (`width`/`height` o `aspect-ratio`) en imágenes de cursos e instructores para reducir CLS.

Ver detalles completos en [`docs/DUDAS.md`](./DUDAS.md).

---

## 3. Estado de tests y mypy

```bash
PYTHONPATH=. pytest
# 41 passed

PYTHONPATH=. mypy src/ --explicit-package-bases --python-executable venv/bin/python
# Success: no issues found in 43 source files
```

**Nota:** Correr `pytest` sin `PYTHONPATH=.` falla con `ModuleNotFoundError: No module named 'src'`. Esto ya era así en el baseline y no fue modificado; el entorno de CI/debería exportar `PYTHONPATH=.` o usar `pytest.ini`.

---

## 4. Próximos pasos recomendados

1. **Revisar `docs/DUDAS.md`** y priorizar las decisiones de alto nivel junto al equipo comercial/contenido.
2. **Auditar Google Search Console/logs** para completar `data/redirects.yaml` con URLs legacy que necesiten redirección 301.
3. **Definir criterios de indexación** para lecciones del LMS y, en caso de indexarlas, generar sitemap de lecciones.
4. **Medir el bundle CSS** (`static/css/index.css`) y evaluar purga de Tailwind o extracción de crítico.
5. **Completar dimensiones de imágenes** en los datos de cursos/instructores o fijar `aspect-ratio` en CSS para mejorar CLS.
6. **Expandir landings** con contenido específico solo para localidades y sectores con potencial comercial real.
7. **Hacer merge de `feature/seo-optimizacion` a `main`** tras review y dejar que el deploy automático de GitHub Actions publique los cambios.

---

## 5. Archivos modificados

- `src/domain/models.py`
- `src/application/data_service.py`
- `src/infrastructure/fastapi/dependencies.py`
- `src/infrastructure/fastapi/app.py`
- `src/infrastructure/fastapi/routes/main_routes.py`
- `templates/index.html`
- `templates/partials/components/service_card.html`
- `templates/partials/components/contact_form.html`
- `templates/contact.html`
- `templates/cursos/instructor.html`
- `templates/cursos/list.html`
- `templates/cursos/detail.html`
- `data/contenido.yaml`
- `data/redirects.yaml` (nuevo)
- `static/humans.txt` (nuevo)
- `tests/test_seo.py`
- `tests/test_additional_routes.py`
- `docs/DUDAS.md` (nuevo)
- `docs/SEO_OPTIMIZACION.md` (nuevo)
