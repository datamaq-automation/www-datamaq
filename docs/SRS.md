# Especificación de Requisitos del Sistema (SRS) - Datamaq

## Contexto de Migración
Replicar la UI/UX de la versión legacy (Vue.js) bajo arquitectura SSR para optimización SEO.

## 1. Funcionalidades Críticas
- **Landing Page SSR:** SEO optimizado, contenido dinámico desde YAML.
- **Cotizador (Wizard UI):** 
    - **Estrategia:** Multi-paso basado en rutas/parámetros (SSR) para mantener estado y SEO en cada etapa.
    - **UX:** Uso de transiciones CSS para emular la fluidez de Vue.
- **RASA Action Server:** Soporte para lógica de negocio del bot.

## 2. Requisitos No Funcionales
- **Performance:** LCP < 2.5s.
- **Fidelidad:** Coincidencia visual del 100% con el diseño original.

---

## 3. Requisitos No Funcionales — SEO y Rendimiento

> Derivados del informe de auditoría SEO técnica. Cada requisito referencia el hallazgo correspondiente.

### 3.1 Requisitos P1 — Críticos

#### R-SEO-01 — Reducir CSS render-blocking
- **Descripción:** La carga de estilos en el `<head>` no debe bloquear el renderizado del contenido above-the-fold.
- **Criterio de aceptación:**
  - El CSS crítico del above-the-fold se entrega inline en el `<head>`.
  - El CSS no crítico se carga de forma diferida o no bloqueante.
  - `index.css` se fragmenta o reduce para no incluir Bootstrap Icons completos ni estilos Tailwind remanentes sin uso.
  - Lighthouse no reporta "Eliminar recursos que bloquean el renderizado" como problema principal.
- **Prioridad:** P1.
- **Referencia:** Informe SEO, oportunidad #1.

#### R-SEO-02 — Diferenciar contenido de páginas dinámicas
- **Descripción:** Las páginas de localidad e industria deben aportar valor de contenido único suficiente para evitar ser clasificadas como thin content o contenido duplicado.
- **Criterio de aceptación:**
  - `data/geografia.yaml` e `industrias.yaml` permiten definir bloques de contenido específicos (casos de uso, equipos recomendados, beneficios, FAQs sectoriales, og_image).
  - El template `index.html` renderiza esos bloques solo cuando existen en el contexto.
  - Google Search Console no reporta alertas de "Contenido escaso" ni "Contenido duplicado" para estas URLs.
- **Prioridad:** P1.
- **Referencia:** Informe SEO, oportunidad #2.

#### R-SEO-03 — Normalización de URLs
- **Descripción:** Las URLs canónicas deben ser accesibles de forma única; las variantes deben redirigir con 301/308.
- **Criterio de aceptación:**
  - Las peticiones `http://` redirigen a `https://`.
  - Las variantes con o sin `www` redirigen a la versión canónica elegida.
  - Las variantes con trailing slash redirigen a la versión sin slash (consistente con rutas actuales).
  - La etiqueta `<link rel="canonical">` coincide con la URL final 200.
- **Prioridad:** P1.
- **Referencia:** Informe SEO, oportunidad #3.

### 3.2 Requisitos P2 — Mejora

#### R-SEO-04 — Evitar FOIT en icon fonts
- **Descripción:** Los icon fonts deben renderizarse con `font-display: swap` o reemplazarse por SVG inline para evitar texto invisible durante la carga.
- **Criterio de aceptación:**
  - Lighthouse no reporta "Evitar texto invisible durante la carga de la fuente web".
  - Los iconos se visualizan correctamente en primera carga.
- **Prioridad:** P2.
- **Referencia:** Informe SEO, oportunidad #4.

#### R-SEO-05 — Logo de Schema.org cuadrado
- **Descripción:** La entidad `Organization` del JSON-LD debe referenciar una imagen de logo cuadrada representativa de marca, no el favicon.
- **Criterio de aceptación:**
  - Se agrega un archivo de logo cuadrado (mínimo 112×112 px) en estáticos.
  - El Schema.org pasa la validación de Rich Results Test / Schema Markup Validator sin errores en el campo `logo`.
- **Prioridad:** P2.
- **Referencia:** Informe SEO, oportunidad #5.

#### R-SEO-06 — Open Graph por página dinámica
- **Descripción:** Las páginas de localidad e industria deben poder configurar su propia imagen Open Graph desde YAML.
- **Criterio de aceptación:**
  - `data/geografia.yaml` e `industrias.yaml` soportan un campo opcional `og_image`.
  - Si no se define, se mantiene la imagen por defecto de `data/contenido.yaml`.
  - Facebook Sharing Debugger y LinkedIn Post Inspector muestran la imagen correcta por URL.
- **Prioridad:** P2.
- **Referencia:** Informe SEO, oportunidad #6.

#### R-SEO-07 — Definir indexabilidad de términos y condiciones
- **Descripción:** Definir si `/terminos-y-condiciones` debe ser indexable.
- **Criterio de aceptación:**
  - Se documenta la decisión de estrategia.
  - Se aplica la meta robots acordada (`index,follow` o `noindex,follow`) de forma consistente.
- **Prioridad:** P2.
- **ESTADO:** BORRADOR.
- **Información faltante:** decisión de negocio sobre si el contenido legal debe aparecer en resultados de búsqueda.
- **Referencia:** Informe SEO, oportunidad #7.

#### R-SEO-08 — Agregar hreflang x-default
- **Descripción:** El sitio debe declarar `hreflang="x-default"` además del `hreflang="es_AR"` existente.
- **Criterio de aceptación:**
  - Cada página incluye ambas etiquetas `alternate` apuntando a su canonical.
  - No hay conflictos de hreflang reportados por herramientas de validación.
- **Prioridad:** P2.
- **Referencia:** Informe SEO, oportunidad #8.

### 3.3 Requisitos futuros — P3

> Optimizaciones de menor impacto inmediato. Pueden abordarse una vez resueltos P1 y P2.

#### R-SEO-09 — Limpiar preconnects a Google Fonts
- **Descripción:** Eliminar los hints de preconnect a `fonts.googleapis.com` y `fonts.gstatic.com` si no se cargan fuentes de Google, o agregar la hoja de estilos correspondiente si se planea usarlas.
- **Prioridad:** P3.
- **Referencia:** Informe SEO, oportunidad #9.

#### R-SEO-10 — Favicon en múltiples formatos
- **Descripción:** Proveer favicon en PNG/ICO además del SVG actual para mayor compatibilidad.
- **Prioridad:** P3.
- **Referencia:** Informe SEO, oportunidad #10.

#### R-SEO-11 — Definir estado del beacon de Cloudflare
- **Descripción:** Activar o eliminar el script comentado de Cloudflare beacon en `index.html`.
- **Prioridad:** P3.
- **Referencia:** Informe SEO, oportunidad #11.

---

## 4. Trazabilidad

- Cada requisito R-SEO-XX debe tener su correspondiente tarea en `docs/TODO.md`.
- Las decisiones de arquitectura asociadas deben reflejarse en `docs/architecture.md`.
- La estrategia de contenido debe mantenerse en `docs/seo_strategy.md`.
