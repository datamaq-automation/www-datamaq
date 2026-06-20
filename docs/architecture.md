# Arquitectura del Sistema - Datamaq

## Visión General
Migración de SPA (Vue.js) a SSR (FastAPI + Jinja2) priorizando SEO, performance (Core Web Vitals) y simplicidad operativa sin sistemas de compilación de assets.

## Flujo de Datos y Estructura
1.  **Backend:** FastAPI inyecta datos desde archivos YAML (`/data/*.yaml`) en el contexto de Jinja2.
2.  **Frontend (SSR):**
    - **Metodología HTML-first:** Definición de estructuras semánticas limpias mediante componentes Jinja2 (`templates/partials/*.html`).
    - **Estilizado (Pure CSS):** Uso de CSS nativo, sin Tailwind ni preprocesadores que requieran compilación en tiempo de despliegue.
    - **Interactividad (Progressive Enhancement):** Vanilla JS inyectado mediante scripts modulares (`static/js/`) para interacciones basadas en estados (`.is-active`).

## Integración RASA
- Acción como **Action Server**.
- Endpoint: `/webhook`.
- Puerto: 5006.

## Infraestructura y CD
- Despliegue automático vía GitHub Actions.
- Script: `scripts/deploy-server.sh`.
- Servicio Systemd: Manejo directo de Uvicorn (sin capas de compilación).

---

## SEO Técnico — Estado post-auditoría

> Refleja el diagnóstico del informe de auditoría SEO técnica.

### Componentes SEO implementados

- **Rutas principales:** `/`, `/contact`, `/terminos-y-condiciones`, `/robots.txt`, `/sitemap.xml`.
- **Rutas dinámicas SEO:**
  - `/{provincia}/{municipio}/{localidad}.html` → `seo_routes.py`.
  - `/industria/{industria}.html` → `industry_routes.py`.
- **Generación de metadatos:** macro `head_seo` en `templates/partials/head.html` inyecta title, description, Open Graph, Twitter Cards, canonical, hreflang y JSON-LD.
- **Canonicalización:** función `canonical_url()` en `src/infrastructure/fastapi/utils/seo.py` fuerza HTTPS y elimina query params.
- **Sitemap dinámico:** generado en `main_routes.py` a partir de `data/geografia.yaml` e `industrias.yaml`.
- **Control de indexabilidad:** preview de componentes y errores no-404 reciben `X-Robots-Tag: noindex, nofollow`; 404 usa `noindex,follow`.
- **Cache de estáticos:** `CachedStaticFiles` aplica `max-age=604800` en producción y `no-cache` en desarrollo.
- **Cache busting:** parámetro `?v=` basado en hash corto de Git (producción) o timestamp (desarrollo).

### Gaps arquitectónicos detectados

| # | Gap | Ubicación | Referencia informe |
|---|-----|-----------|-------------------|
| 1 | **CSS bloqueante en `<head>`** | `templates/partials/head.html` carga 6 hojas CSS en serie, incluyendo `index.css` de ~122 KB. | Oportunidad #1. |
| 2 | **Fuente de iconos con `font-display: block`** | `static/css/index.css` declara Bootstrap Icons con FOIT. | Oportunidad #4. |
| 3 | **Preconnect a dominios no utilizados** | `head.html` incluye preconnect a `fonts.googleapis.com` y `fonts.gstatic.com` sin cargar fuentes. | Oportunidad #9. |
| 4 | **Páginas dinámicas comparten template** | `index.html` es usado por home, localidad e industria con mínima diferenciación. | Oportunidad #2. |
| 5 | **Open Graph imagen única** | `og:image` proviene de `data/contenido.yaml` y no admite variante por página dinámica. | Oportunidad #6. |
| 6 | **Schema.org `logo` como favicon** | JSON-LD de Organization usa `favicon.svg`. | Oportunidad #5. |
| 7 | **Favicon solo SVG** | `head.html` solo provee favicon SVG. | Oportunidad #10. |
| 8 | **Hreflang sin `x-default`** | `head.html` solo declara `es_AR`. | Oportunidad #8. |
| 9 | **Beacon de terceros inactivo** | Script de Cloudflare comentado en `index.html`. | Oportunidad #11. |

### Decisiones de infraestructura pendientes

#### 1. Normalización de URLs

- **Situación actual:** FastAPI no incluye middleware ni redirecciones para forzar HTTPS, eliminar/agregar trailing slash ni canonicalizar www/no-www. La canonicalización se limita a la etiqueta `<link rel="canonical">`.
- **Dependencia:** el comportamiento real en producción depende del reverse proxy (Nginx/Cloudflare).
- **Decisión pendiente:** validar si el reverse proxy ya realiza estas redirecciones. De no ser así, se deberá agregar una capa de normalización en la aplicación.

#### 2. Comportamiento esperado de un middleware de normalización (si se implementa)

> **Nota:** esta sección documenta requisitos de comportamiento. No incluye código de implementación.

Si se decide agregar un middleware de normalización en FastAPI, su comportamiento debería ser:

- **Protocolo:** redirigir `http://` a `https://` con **HTTP 301**.
- **Trailing slash:** elegir una convención (sin slash, consistente con las rutas actuales `/contact`, `/terminos-y-condiciones`) y redirigir `/contact/` → `/contact` con **HTTP 301**.
- **WWW:** elegir versión canónica (`www` o `non-www`) y redirigir la contraria con **HTTP 301**.
- **Query params:** mantenerlos o descartarlos según la canonicalización actual (`canonical_url()` los elimina).
- **Exclusiones:** no redirigir rutas de API que requieran POST con body ni el endpoint `/webhook` de RASA si su contrato lo prohíbe.
- **Headers de seguridad:** considerar agregar `Strict-Transport-Security` si se fuerza HTTPS.

#### 3. Estrategia de assets estáticos

- **Situación actual:** todos los CSS se sirven como archivos independientes sin minificación ni bundling en despliegue.
- **Decisión pendiente:** decidir si se mantiene el enfoque "sin build" o si se incorpora un paso de minificación/fragmentación crítica para reducir el impacto en Core Web Vitals.

#### 4. Fuentes e iconos

- **Situación actual:** Bootstrap Icons se cargan desde CDN dentro de `index.css` mediante `@font-face`.
- **Decisión pendiente:** decidir si se mantiene el font o se migran los pocos iconos usados a SVG inline, eliminando una dependencia externa y el FOIT.

---

## Notas de trazabilidad

- Toda mejora sobre SEO técnico debe reflejarse en `docs/TODO.md` y `docs/SRS.md`.
- Los cambios de infraestructura deben coordinarse con la documentación de despliegue (`docs/CD.md`).
