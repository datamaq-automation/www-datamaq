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
- **Archivos afectados:** `redirects.yaml`, `data_service.py`

---

## Duda de alto nivel: Reorganización de `data/` por Bounded Contexts
- **Contexto:** La carpeta `data/` mezcla contenidos globales de diseño y marca (`contenido.yaml`), base de datos geográfica (`geografia.yaml`), redirecciones (`redirects.yaml`), marketing y SEO (`landing_content.yaml`) y entidades core del dominio (cursos y casos). Esto dificulta ver los límites del negocio (Bounded Contexts) a nivel físico.
- **Opciones consideradas:**
  - **A.** Mantener la estructura plana actual en la carpeta `data/`.
  - **B.** Reorganizar en subcarpetas temáticas que reflejen el negocio: `data/core/` (cursos, casos), `data/marketing/` (landing_content, geografia, industrias) y `data/config/` (redirects, contenido).
- **Recomendación del agente:** Opción **B**. Clarifica la arquitectura y grita el dominio del negocio de inmediato.
- **Bloqueo:** Requiere actualizar todas las rutas de inicialización del `DataService` en la configuración y scripts de despliegue.
- **Impacto estimado:** Medio (Mantenibilidad).
- **Archivos afectados:** Todos los archivos en `data/` y `src/infrastructure/fastapi/dependencies.py`.

---

## Duda de alto nivel: Separación de concerns en YAML (SEO/Config vs Editorial)
- **Contexto:** En `contenido.yaml` conviven metadatos de SEO (`seo: title, description`), reglas de renderizado/diseño (nombres de iconos de Bootstrap, llamadas a la acción `cta`, cantidad de pasos) y contenido netamente editorial (preguntas frecuentes `faq`, párrafos descriptivos). Esto confunde los concerns y expone a errores técnicos al modificar textos.
- **Opciones consideradas:**
  - **A.** Mantener el diseño monolítico actual en `contenido.yaml`.
  - **B.** Dividir en archivos de responsabilidad única: `data/site_seo.yaml` (SEO), `data/site_brand.yaml` (ajustes técnicos de marca) y `data/editorial_home.yaml` (copys del home).
- **Recomendación del agente:** Opción **B**. Aísla fallos y permite flujos de edición separados.
- **Bloqueo:** Exige reestructurar por completo los esquemas Pydantic en `models.py` y actualizar el `DataService`.
- **Impacto estimado:** Medio (Mantenibilidad).
- **Archivos afectados:** `contenido.yaml`, `src/domain/models.py`, `src/application/data_service.py`.

---

## Duda de alto nivel: Creación de Value Objects Enriquecidos
- **Contexto:** Actualmente `models.py` valida tipos de datos elementales con Pydantic. Las reglas específicas de negocio (ej: que un slug de curso o lección deba seguir exactamente el regex `^[a-z0-9-]+$`, o que un email deba validarse de forma corporativa) no están encapsuladas en Value Objects ricos de dominio bajo `src/domain/value_objects/`.
- **Opciones consideradas:**
  - **A.** Mantener las validaciones inline con Pydantic `Field` tal como se implementó de forma incremental.
  - **B.** Definir clases de Value Objects ricos (ej: `Slug`, `Price`, `Email`) con su lógica de validación e inicialización independiente en la capa de dominio.
- **Recomendación del agente:** Opción **B**. Robustece el código y reduce la duplicación de validadores en diferentes modelos de Pydantic.
- **Bloqueo:** Requiere una revisión profunda de tipos que podría generar incompatibilidades de deserialización en YAMLs existentes.
- **Impacto estimado:** Medio (Arquitectura Limpia).
- **Archivos afectados:** `src/domain/models.py`, `src/domain/value_objects/`.

---

## Duda de alto nivel: Sistema de Versionado y Migración de Datos YAML
- **Contexto:** Al evolucionar los esquemas de dominio en Pydantic, los archivos YAML históricos que no cuenten con las nuevas claves obligatorias fallarán. Actualmente no hay un pipeline o CLI para migrar o validar esquemas históricos en disco.
- **Opciones consideradas:**
  - **A.** Realizar migraciones manuales en los archivos YAML cada vez que cambien los modelos.
  - **B.** Desarrollar una herramienta CLI que analice los esquemas Pydantic y autocomplete/corrija los archivos YAML en disco.
- **Recomendación del agente:** Opción **B**. Asegura estabilidad y facilita la edición de contenidos por autores no técnicos.
- **Bloqueo:** Requiere el desarrollo de tooling e infraestructura adicional de compilación.
- **Impacto estimado:** Alto (Seguridad en Despliegues).
- **Archivos afectados:** Tooling / scripts de desarrollo.
