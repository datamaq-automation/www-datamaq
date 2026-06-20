# Estrategia SEO - Datamaq

La migración de Vue SPA a **FastAPI Jinja2 SSR** es la piedra angular de esta estrategia, eliminando las barreras de indexación de las aplicaciones de una sola página.

1. **Renderizado en Servidor (SSR):** Garantiza que el 100% del contenido sea visible para los rastreadores desde el primer byte.
2. **Técnica:** Sitemap, robots.txt, caché HTTP.
3. **Semántica:** Datos estructurados (Schema.org) y contenido alineado con AAIERIC para autoridad de marca.
4. **Presencia:** Meta Tags y Open Graph dinámicos.
5. **Experiencia:** Core Web Vitals (LCP optimizado mediante SSR, sin bloqueos de renderizado JS).
6. **Autoridad:** Alineación con lineamientos oficiales de AAIERIC para generar confianza.

## Investigación básica de keywords

### Keywords principales recomendadas

| # | Keyword | Intención de búsqueda | Aplicación sugerida |
|---|---------|------------------------|------------------------|
| 1 | **monitoreo de energía industrial** | Información / servicio | Página home, páginas de industria, H1 de servicios |
| 2 | **captura de datos operativos** | Información / servicio | Home, páginas de localidad, descripciones de servicio |
| 3 | **IoT industrial** | Información / tecnología | Home, páginas de industria, contenido de perfil |
| 4 | **equipos IoT para medición de energía** | Compra / servicio | Páginas de industria, tarjetas de servicio, CTA |
| 5 | **digitalización de planta** / **industria 4.0 Argentina** | Estrategia / transformación | Home, about, contenido de autoridad |

### Keywords secundarias y de cola larga

- medición de energía industrial
- medidores de energía trifásica
- análisis de consumo energético
- captura de datos de producción
- monitoreo remoto de procesos industriales
- sensores industriales para producción
- eficiencia energética industrial
- sistemas SCADA para industria
- automatización industrial Argentina
- transformación digital industrial

### Keywords locales (para páginas SEO por localidad)

- monitoreo de energía industrial en {localidad}
- captura de datos operativos en {localidad}
- instalación de equipos IoT en {localidad}
- digitalización de planta en {localidad}
- servicios técnicos IoT en {localidad}

### Mapeo preliminar de keywords a páginas

| Página | Keyword principal | Uso |
|-------------|-------------------|-----|
| Home | monitoreo de energía industrial + captura de datos operativos | Título, H1, descripción |
| /industria/{industria}.html | IoT industrial + {industria} | Título, H1, descripción |
| /{prov}/{mun}/{loc}.html | monitoreo de energía industrial en {loc} | Título, H1, descripción |
| /contact | consultoría técnica IoT | Título, descripción |

## Notas metodológicas

- Esta investigación se realizó con búsquedas web públicas; no se utilizaron herramientas de pago como Ahrefs, SEMrush o Google Keyword Planner.
- Los volúmenes de búsqueda son estimaciones cualitativas basadas en la frecuencia de aparición de los términos en contenido especializado y competencia.
- La selección final de keywords debe validarse contra los objetivos comerciales de DataMaq y el margen/prioridad de cada servicio.

---

## Diagnóstico técnico

> Estado post-auditoría. Cada ítem referencia el informe de auditoría SEO técnica.

### Aspectos técnicos sanos

- **SSR completo:** el contenido crítico se renderiza en HTML inicial. (Ver informe SEO, constatación general.)
- **Indexabilidad básica:** `robots.txt` permite todo, 404 y preview de componentes devuelven `noindex`, y los errores HTTP no-404 incluyen `X-Robots-Tag: noindex, nofollow`. (Oportunidades #1-contexto, #3-contexto.)
- **Canonicals:** se generan forzando HTTPS y eliminando query params en todas las rutas principales. (Oportunidad #3.)
- **Sitemap dinámico:** incluye home, contacto, términos, localidades e industrias. (Oportunidad #3-contexto.)
- **Metadatos dinámicos:** title, description, Open Graph y Twitter Cards están presentes. (Oportunidades #6, #8.)

### Aspectos técnicos a corregir

- **CSS bloqueante:** se cargan 6 hojas CSS en el `<head>` (~159 KB totales), siendo `index.css` de ~122 KB con Bootstrap Icons completos y estilos remanentes de Tailwind. Esto impacta LCP y FCP. (Oportunidad #1.)
- **`font-display: block` en Bootstrap Icons:** produce Flash of Invisible Text. (Oportunidad #4.)
- **Preconnects a Google Fonts sin uso:** existen hints de conexión a fuentes que no se cargan. (Oportunidad #9.)
- **Favicon solo SVG:** compatibilidad limitada en Safari y navegadores antiguos. (Oportunidad #10.)
- **Cloudflare beacon comentado:** código inactivo en `index.html`. (Oportunidad #11.)

### Aspectos de contenido y estructura

- **Páginas dinámicas comparten template:** home, localidades e industrias usan `index.html` con ~90 % de contenido idéntico. (Oportunidad #2.)
- **Open Graph imagen única:** todas las páginas comparten `og-default.jpg`. (Oportunidad #6.)
- **Schema.org `logo` usa favicon:** la entidad Organization referencia `favicon.svg` en lugar de un logo cuadrado. (Oportunidad #5.)
- **Hreflang sin `x-default`:** solo se declara `es_AR`. (Oportunidad #8.)

### Arquitectura de URLs

- No hay middleware en FastAPI que normalice HTTP→HTTPS, trailing slash ni www/no-www. La canonicalización depende exclusivamente del reverse proxy en producción. (Oportunidad #3.)

---

## Riesgos críticos

| Riesgo | Impacto en leads | Origen |
|--------|------------------|--------|
| **Pérdida de visibilidad por thin content** | Las páginas de localidad e industria, clave para captar tráfico cualificado, pueden no posicionar porque su contenido propio es mínimo. | Oportunidad #2. |
| **LCP alto por CSS bloqueante** | Una mala experiencia de carga reduce la tasa de conversión del formulario de contacto y aumenta el rebote. | Oportunidad #1. |
| **Contenido duplicado por falta de normalización** | Si el reverse proxy no redirige, Google podría indexar múltiples versiones de la misma URL (`http`/`https`, `/contact`/`/contact/`), dispersando autoridad. | Oportunidad #3. |
| **Imagen OG genérica** | Menor CTR desde resultados sociales y búsqueda, menos tráfico de calidad hacia las páginas de industria/localidad. | Oportunidad #6. |

---

## Oportunidades de contenido

> Estrategia de enriquecimiento de páginas dinámicas sin redactar textos definitivos. El objetivo es aumentar el valor único de cada URL y su relevancia para keywords sectoriales/locales.

### Enfoque general

- Mantener la home como el "hub" de servicios genéricos.
- Convertir las páginas de **localidad** en "landing de cobertura técnica" añadiendo bloques propios.
- Convertir las páginas de **industria** en "landing sectorial" añadiendo bloques propios.

### Estructura de contenido propuesta para localidades

Cada entrada en `data/geografia.yaml` podría extenderse con campos opcionales que se rendericen solo si existen:

- `casos_locales`: casos de uso típicos de la zona (sin nombres de clientes si no hay permiso).
- `equipos_recomendados`: equipos compatibles con las industrias predominantes de la zona.
- `cobertura_logistica`: alcance de visitas técnicas o soporte remoto.
- `contexto_regional`: normativas o particularidades energéticas/industriales de la provincia/municipio.
- `og_image`: imagen Open Graph específica para la localidad.

### Estructura de contenido propuesta para industrias

Cada entrada en `data/industrias.yaml` podría extenderse con:

- `casos_sectoriales`: problemáticas comunes de la industria y cómo se resuelven con captura de datos.
- `equipos_sectoriales`: equipos IoT o medidores típicamente usados en el sector.
- `beneficios_clave`: diferenciadores específicos para esa industria.
- `preguntas_frecuentes_sectoriales`: FAQs adicionales que solo se muestren en la página de industria.
- `og_image`: imagen Open Graph específica para la industria.

### Criterio de implementación

- Los bloques deben ser opcionales: si no existen en YAML, no se renderizan.
- No se modificarán los textos existentes de home; solo se añadirán secciones condicionales en `index.html` para localidad/industria.
- La decisión sobre qué industrias/localidades enriquecer primero dependerá de potencial de leads y facilidad de generar contenido técnico.

---

## Decisiones pendientes

> Antes de cualquier implementación deben resolverse las siguientes decisiones estratégicas.

1. **Indexabilidad de `/terminos-y-condiciones`**
   - *Detección:* la página legal actualmente es `index,follow`. (Oportunidad #7.)
   - *Relevancia:* un contenido legal indexado puede atraer tráfico no comercial; un `noindex` lo excluye de resultados.
   - *Decisión pendiente:* definir si se desea que la página aparezca en buscadores o se prefiere concentrar el crawl presupuesto en páginas de conversión.

2. **Responsabilidad de normalización de URLs**
   - *Detección:* la aplicación no normaliza URLs. (Oportunidad #3.)
   - *Relevancia:* evitar contenido duplicado y consolidar señales de ranking.
   - *Decisión pendiente:* confirmar si Nginx/Cloudflare ya realiza estas redirecciones. Si es así, no se requiere middleware en FastAPI; si no, se deberá implementar como respaldo defensivo.

3. **Priorización de industrias y localidades para enriquecimiento de contenido**
   - *Detección:* solo existen 2 localidades y 4 industrias. (Contexto del informe.)
   - *Relevancia:* el enriquecimiento requiere esfuerzo de redacción técnica.
   - *Decisión pendiente:* seleccionar qué industrias y localidades se enriquecen primero según potencial comercial.

---

## Métricas de validación

| Mejora | KPI / Herramienta | Criterio de éxito tentativo |
|--------|-------------------|----------------------------|
| CSS crítico y carga no bloqueante | PageSpeed Insights / Lighthouse | LCP < 2.5 s en móvil; FCP mejora; CLS estable. |
| Enriquecimiento de páginas dinámicas | Google Search Console | Incremento de impresiones/clics para URLs de industria/localidad; sin alertas de "Contenido escaso". |
| Normalización de URLs | Screaming Frog / curl | Solo responde código 200 la URL canónica; variantes devuelven 301/308. |
| `font-display: swap` | Lighthouse "Avoid invisible text during webfont load" | Eliminación del warning. |
| Logo Schema.org | Google Rich Results Test / Schema Markup Validator | Sin errores en entidad Organization; logo reconocido. |
| `og:image` por página | Facebook Sharing Debugger / LinkedIn Post Inspector | Previsualización correcta y diferenciada por URL. |
| `hreflang="x-default"` | Google Search Console / flang tag checker | Etiqueta presente y sin conflictos. |
| Indexabilidad de términos | Google Search Console | Decisión documentada y aplicada consistentemente. |
