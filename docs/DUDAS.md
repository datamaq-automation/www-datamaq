# Dudas de alto nivel — www-datamaq

Este documento reúne las decisiones estratégicas, de arquitectura y de negocio que no se implementaron de forma autónoma por involucrar políticas de negocio, riesgo de cambios estructurales o falta de contexto suficiente. Cada ítem incluye opciones consideradas, recomendación del agente y el impacto estimado.

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
