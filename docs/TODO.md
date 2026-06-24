# TODO.md — Datamaq

**Estado del proyecto:** Etapa 1 (Estabilización del deploy) ✅ completada.  
 Etapa 2 (GitHub Actions) ✅ completada. Deploy automático activo con usuario `datamaq`, SSH por clave, Python 3.12 y rollback implementado.  
 **Iteración actual:** SEO técnico + adopción de DDD / Arquitectura Limpia.  
 **Bloqueos activos:** Ninguno.

---

## 🔥 P0 — Crítico / Bloqueante

_Ninguno. El pipeline de deploy y la infraestructura base están estables._

---

## 📌 P1 — Crítico (Implementación requerida)

### SEO
- [ ] **P1-SEO-02** Diferenciar contenido de páginas dinámicas (localidad e industria) para mitigar *thin content* y contenido duplicado.
  - *Referencia:* Informe SEO, oportunidad #2.
  - *Nota:* Home, localidades e industrias comparten el mismo template `index.html` con ~90 % de contenido idéntico.

- [x] **P1-SEO-03** Normalizar URLs (HTTP→HTTPS, trailing slash, www/no-www).
  - *Referencia:* Informe SEO, oportunidad #3.
  - *Estado:* Completado. Middleware `canonical_redirect_middleware` en `src/infrastructure/fastapi/middleware.py`. Actúa como respaldo cuando el reverse proxy envía `X-Forwarded-Proto: http`.

### DDD / Arquitectura Limpia
- [ ] **P1-DDD-01** Publicar evento de dominio `LeadSubmitted` al persistir un lead, y suscribir a Chatwoot como consumidor.
- [ ] **P1-DDD-02** Mover reglas de validación de negocio ("email o teléfono requerido") desde el schema Pydantic hacia la entidad de dominio `Lead`.

---

## 📋 P2 — Mejora (Backlog inmediato)

### SEO
- [ ] **P2-SEO-05** Reemplazar el favicon SVG usado como `logo` en Schema.org por una imagen cuadrada representativa de marca.
  - *Referencia:* Informe SEO, oportunidad #5.

- [ ] **P2-SEO-06** Permitir configurar `og:image` específico por localidad e industria en los archivos YAML.
  - *Referencia:* Informe SEO, oportunidad #6.

- [ ] **P2-SEO-07** Agregar `hreflang="x-default"` junto al `hreflang="es_AR"` existente.
  - *Referencia:* Informe SEO, oportunidad #8.

### DDD / Arquitectura Limpia
- [ ] **P2-DDD-03** Aplicar patrón Repository en `DataService` para evitar lectura de YAML en cada request (caché de contenido estático).

### Cursos (LMS - LearnPress-like)
- [x] **P2-LMS-01** Crear archivo de datos `data/cursos.yaml` con la estructura de cursos, secciones y lecciones.
- [x] **P2-LMS-02** Implementar modelos de validación Pydantic para Cursos en `src/domain/models.py`.
- [x] **P2-LMS-03** Modificar `DataService` en `src/application/data_service.py` para soportar la carga y obtención de cursos con caché.
- [x] **P2-LMS-04** Desarrollar las rutas de cursos (`/cursos`, `/cursos/{curso_slug}`, `/cursos/{curso_slug}/{leccion_slug}`) en `src/infrastructure/fastapi/routes/course_routes.py`.
- [x] **P2-LMS-05** Diseñar las plantillas Jinja2 (`list.html`, `detail.html`, `lesson.html`) en `src/infrastructure/fastapi/templates/cursos/`.
- [x] **P2-LMS-06** Crear hoja de estilos CSS nativos `static/css/cursos.css` para el catálogo y el reproductor de lecciones.
- [x] **P2-LMS-07** Implementar interactividad opcional (marcar lección completada, sidebar colapsable, barra de progreso) en `static/js/modules/CourseManager.js`.
- [x] **P2-LMS-08** Agregar marcado estructurado Schema.org (`Course` JSON-LD) e integrar las rutas de cursos al generador dinámico de `sitemap.xml`.
- [x] **P2-LMS-09** Escribir tests unitarios en `tests/test_cursos.py` para validar la carga de YAML, respuestas de endpoints y sitemap.

---

## 🔮 P3 — Optimización futura

### SEO
- [ ] **P3-SEO-09** Eliminar preconnects a Google Fonts si no se cargan fuentes, o agregar la hoja de estilos correspondiente.
  - *Referencia:* Informe SEO, oportunidad #9.

- [ ] **P3-SEO-10** Proveer favicon en formatos PNG/ICO además del SVG actual.
  - *Referencia:* Informe SEO, oportunidad #10.

- [ ] **P3-SEO-11** Definir si se activa o elimina el script comentado de Cloudflare beacon.
  - *Referencia:* Informe SEO, oportunidad #11.

---

## ❓ Decisiones estratégicas pendientes

Items que requieren una decisión de negocio antes de convertirse en tareas técnicas.

- [ ] **DEC-SEO-01** Definir si `/terminos-y-condiciones` debe permanecer indexable (`index,follow`) o pasar a `noindex,follow`.
  - *Referencia:* Informe SEO, oportunidad #7.
  - *Bloqueado por:* Estrategia de contenido legal.

- [ ] **DEC-SEO-02** Confirmar si el reverse proxy de producción (Nginx/Cloudflare) ya realiza redirecciones HTTP→HTTPS y normalización de trailing slash/www.
  - *Referencia:* Informe SEO, oportunidad #3.
  - *Bloqueado por:* Validación de infraestructura. El middleware de respaldo ya está implementado, pero se debe verificar si es redundante.

---

## ✅ Completado (resumen)

- **DevOps / CI-CD:** Etapa 1 y 2 finalizadas. Ver detalles en `docs/TODO.done.md`.
- **P1-SEO-03:** Middleware de normalización de URLs implementado.