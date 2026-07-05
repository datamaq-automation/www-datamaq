# Dudas de alto nivel — www-datamaq

Este documento reúne las decisiones estratégicas, de arquitectura y de negocio que no se implementaron de forma autónoma por involucrar políticas de negocio, riesgo de cambios estructurales o falta de contexto suficiente. Cada ítem incluye opciones consideradas, recomendación del agente y el impacto estimado.

---

## Duda de alto nivel: CSS crítico inline para Above The Fold
- **Contexto:** La Home y las principales landings cargan `index.css` como stylesheet render-blocking. No existe CSS crítico inline para pintar el contenido inicial mientras llega el resto del CSS.
- **Opciones consideradas:**
  - **A.** No inlinear y mantener el archivo externo con caché agresiva.
  - **B.** Extraer manualmente las reglas críticas del hero/header para las 3-4 rutas principales e inlinearlas en `<style>` dentro de `head.html`, cargando el resto de forma asíncrona.
  - **C.** Usar una herramienta de extracción automática de crítico (requiere npm/webpack, prohibido por las restricciones actuales).
- **Recomendación del agente:** Opción **B** solo si se puede automatizar una verificación post-cambio; de lo contrario, **A** es más seguro. No se implementó por el riesgo de romper el estilo inicial si las reglas inline quedan desfasadas del bundle.
- **Bloqueo:** Requiere decisión sobre si se acepta mantener dos fuentes de verdad para los estilos críticos.
- **Impacto SEO estimado:** Medio (LCP/CLS).
- **Archivos afectados:** `templates/partials/head.html`

---

## Duda de alto nivel: Mapeo de URLs legacy de la SPA anterior
- **Contexto:** El sitio anterior era una SPA. No hay tabla de redirecciones 301 por URL; todo 404 desconocido va a `/`. Puede haber URLs indexadas en Google o backlinks apuntando a rutas que ahora pierden su señal.
- **Opciones consideradas:**
  - **A.** Recopilar logs de 404 y crear redirecciones 301 puntuales en FastAPI.
  - **B.** Generar un listado de URLs legacy desde Google Search Console / Analytics y mapearlas a la landing equivalente.
  - **C.** Mantener el wildcard si no hay tráfico significativo hacia URLs antiguas.
- **Recomendación del agente:** Opción **A+B**: auditar 404 reales durante 30 días y redirigir las rutas con tráfico a su contraparte semántica (home, servicio, curso o contacto).
- **Bloqueo:** No se cuenta con los logs históricos ni acceso a Search Console desde este entorno.
- **Impacto SEO estimado:** Medio.
- **Archivos afectados:** `data/config/redirects.yaml`, `data_service.py`
