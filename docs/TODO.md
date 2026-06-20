# Tareas pendientes — Datamaq

## SEO — Iteración actual

> Basado en el informe de auditoría SEO técnica. Cada ítem referencia el hallazgo correspondiente del informe.

### P1 — Crítico

- [ ] **P1-SEO-01** Reducir/fragmentar CSS render-blocking de ~159 KB en `<head>`.
  - *Referencia:* Informe SEO, oportunidad #1.
  - *Nota:* `index.css` pesa ~122 KB e incluye Bootstrap Icons completos + estilos remanentes. Se cargan 6 hojas CSS en serie en el `<head>`.

- [ ] **P1-SEO-02** Diferenciar contenido de páginas dinámicas (localidad e industria) para mitigar thin content y contenido duplicado.
  - *Referencia:* Informe SEO, oportunidad #2.
  - *Nota:* Home, localidades e industrias comparten el mismo template `index.html` con ~90 % de contenido idéntico.

- [ ] **P1-SEO-03** Implementar normalización de URLs en la aplicación (HTTP→HTTPS, trailing slash, www/no-www) o validar que el reverse proxy ya la realice.
  - *Referencia:* Informe SEO, oportunidad #3.
  - *Nota:* Actualmente no hay middleware en FastAPI que redirija a la versión canónica.

### P2 — Mejora

- [ ] **P2-SEO-04** Cambiar `font-display: block` a `swap` (o reemplazar iconos por SVG inline) para eliminar FOIT en Bootstrap Icons.
  - *Referencia:* Informe SEO, oportunidad #4.

- [ ] **P2-SEO-05** Reemplazar el favicon SVG usado como `logo` en Schema.org por una imagen cuadrada representativa de marca.
  - *Referencia:* Informe SEO, oportunidad #5.

- [ ] **P2-SEO-06** Permitir configurar `og:image` específico por localidad e industria en los archivos YAML.
  - *Referencia:* Informe SEO, oportunidad #6.

- [ ] **P2-SEO-07** Agregar `hreflang="x-default"` junto al `hreflang="es_AR"` existente.
  - *Referencia:* Informe SEO, oportunidad #8.

### P3 — Optimización futura

- [ ] **P3-SEO-09** Eliminar preconnects a Google Fonts si no se cargan fuentes, o agregar la hoja de estilos correspondiente.
  - *Referencia:* Informe SEO, oportunidad #9.

- [ ] **P3-SEO-10** Proveer favicon en formatos PNG/ICO además del SVG actual.
  - *Referencia:* Informe SEO, oportunidad #10.

- [ ] **P3-SEO-11** Definir si se activa o elimina el script comentado de Cloudflare beacon.
  - *Referencia:* Informe SEO, oportunidad #11.

---

## Pendientes de decisión

> Items cuya certeza en el informe es "Duda" o "Requiere validación". Requieren una decisión estratégica antes de convertirse en tareas de implementación.

- [ ] **DEC-SEO-01** Definir si `/terminos-y-condiciones` debe permanecer indexable (`index,follow`) o pasar a `noindex,follow`.
  - *Referencia:* Informe SEO, oportunidad #7.
  - *Certeza:* Requiere validación.
  - *Pendiente:* Decisión de estrategia de contenido legal.

- [ ] **DEC-SEO-02** Confirmar si el reverse proxy de producción (Nginx/Cloudflare) ya realiza redirecciones HTTP→HTTPS y normalización de trailing slash/www.
  - *Referencia:* Informe SEO, oportunidad #3.
  - *Certeza:* Requiere validación.
  - *Pendiente:* Validación de infraestructura antes de implementar middleware de respaldo en FastAPI.
