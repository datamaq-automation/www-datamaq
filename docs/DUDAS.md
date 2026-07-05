# Dudas de alto nivel — Optimización SEO

Este documento reúne las decisiones estratégicas y de arquitectura que no se implementaron de forma autónoma por involucrar políticas de negocio, riesgo de cambios estructurales o falta de contexto suficiente. Cada ítem incluye opciones consideradas, recomendación del agente y el motivo por el que quedó pendiente de consulta.

---

## ✅ Resuelta — Redirección wildcard 301 de 404 a `/`
- **Contexto:** El manejador de excepciones de `src/infrastructure/fastapi/app.py` redirigía con HTTP 301 cualquier 404 no estático/no API hacia la Home (`/`). Esto fue heredado de la migración SPA para no perder tráfico, pero generaba "soft 404" y diluía la señal de autoridad de URLs antiguas.
- **Decisión tomada:** Se reemplazó el wildcard 301 por una verdadera respuesta 404 con la plantilla `404.html` (`noindex, follow`). A su vez se creó `data/redirects.yaml` para configurar redirecciones 301 puntuales hacia donde se necesite.
- **Implementación:**
  - `src/infrastructure/fastapi/app.py` consulta `data_service.get_redirects()` antes de servir el 404.
  - Si el path coincide con una clave de `redirects`, responde `301` al destino configurado.
  - Si no coincide, responde `404` con la plantilla existente.
  - `src/application/data_service.py` expone `get_redirects()` y cachea el contenido de `data/redirects.yaml`.
  - Los tests `test_404_has_noindex` y `test_custom_404_page_rendered` se actualizaron para reflejar el nuevo comportamiento.
- **Próximo paso:** Completar `data/redirects.yaml` con las URLs legacy de la SPA que tengan tráfico o backlinks, auditando logs de 404 o Google Search Console.
- **Impacto SEO estimado:** Medio-Alto.

---

## ✅ Resuelta — Indexar o no las páginas de lección individuales
- **Contexto:** Las lecciones (`/cursos/{curso_slug}/{leccion_slug}`) tenían `<meta name="robots" content="noindex, follow">`. Al confirmar que los cursos son **capacitaciones de cortesía** y no el producto principal, la decisión se simplifica.
- **Decisión tomada:** Mantener `noindex, follow` en lecciones individuales. El foco SEO debe estar en la asistencia técnica (visitas en campo + remota), no en captar tráfico educativo para vender cursos.
- **Implementación:** No se requirieron cambios de código; se documenta la política para futuras revisiones.
- **Impacto SEO estimado:** Bajo (evita fragmentar autoridad hacia contenido que no es el negocio).

---

## Duda de alto nivel: Arquitectura de CSS y purga de Tailwind
- **Contexto:** El bundle `static/css/index.css` es la salida compilada de Tailwind CSS v4.2.1. No se mide su peso real ni se conoce el porcentaje de clases no utilizadas. Además, coexisten hojas heredadas (`HomePage.css`, `cursos.css`, etc.) cargadas de forma plana.
- **Opciones consideradas:**
  - **A.** Dejar el build actual y confiar en la compresión GZip + caché.
  - **B.** Auditar el bundle, configurar el content de Tailwind para purgar clases no usadas y, si aplica, separar CSS crítico Above The Fold.
  - **C.** Reorganizar `static/css/` por dominio (home, cursos, componentes, utilidades) en lugar del esquema plano actual.
- **Recomendación del agente:** Opción **B** primero (medición + purga), y **C** solo si se justifica por mantenibilidad. No eliminar Bootstrap/base sin validar que ningún template dependa de él.
- **Bloqueo:** Cambiar el build de Tailwind o la estructura de CSS implica tocar el pipeline de assets, posiblemente agregar scripts de build y verificar visualmente cada página. Esto excede el alcance de una optimización de bajo nivel segura.
- **Impacto SEO estimado:** Medio (Core Web Vitals).

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

---

## Duda de alto nivel: Expansión de landings geográficas e industriales
- **Contexto:** Hoy existen dos localidades (`Garín`, `Belén de Escobar`) y una industria (`Industria Gráfica`). El sitemap y las landings están automatizados, por lo que agregar más datos YAML escalaría el número de URLs indexables.
- **Opciones consideradas:**
  - **A.** Mantener el alcance actual mientras se consolida la autoridad del dominio.
  - **B.** Expandir progresivamente a municipios/industrias relevantes con contenido diferenciado (no solo rellenar el template con otro nombre).
  - **C.** Crear landings de provincia/municipio además de localidad.
- **Recomendación del agente:** Opción **B** con criterio de calidad: cada nueva landing debe tener al menos un párrafo de contexto sectorial/geográfico único. Evitar generar miles de páginas con descripciones casi idénticas.
- **Bloqueo:** Se desconoce el mercado objetivo y la capacidad de generar contenido específico. Decidirlo requiere input comercial.
- **Impacto SEO estimado:** Alto.

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

---

## Duda de alto nivel: Estrategia de contenido para autoridad de dominio
- **Contexto:** El sitio actual es principalmente comercial + LMS. No hay sección de blog, casos de éxito o guías técnicas que generen backlinks orgánicos.
- **Opciones consideradas:**
  - **A.** Mantener el sitio como está y confiar en las landings locales/industriales.
  - **B.** Crear una sección `/blog` o `/casos` con artículos técnicos (monitoreo de energía, casos de IoT industrial, tutoriales Python).
  - **C.** Convertir las lecciones indexadas del LMS en contenido puerta de entrada para búsquedas educativas.
- **Recomendación del agente:** Opción **B+C**: publicar contenido técnico propio y permitir que el LMS funcione como hub educativo, enlazando naturalmente hacia los servicios.
- **Bloqueo:** Requiere plan editorial, recursos de redacción técnica y definición de voz de marca.
- **Impacto SEO estimado:** Alto.

---

## Duda de alto nivel: Dimensiones explícitas en imágenes de cursos e instructores
- **Contexto:** Las tarjetas de curso, la imagen destacada del curso y las fotos de instructores no incluyen atributos `width`/`height`. Aunque tienen `loading` y `decoding`, la ausencia de dimensiones puede contribuir a CLS si el CSS no fija un aspect-ratio estable.
- **Opciones consideradas:**
  - **A.** Agregar `width`/`height` al modelo de curso e instructor y propagarlos desde los archivos YAML.
  - **B.** Resolver dimensiones en tiempo de build/servidor leyendo los metadatos de las imágenes.
  - **C.** Definir `aspect-ratio` en CSS y no tocar los datos.
- **Recomendación del agente:** Opción **A** si se conocen las dimensiones reales; opción **C** como solución rápida mientras se completan los datos.
- **Bloqueo:** No se dispone de las dimensiones reales de cada imagen en los archivos de datos, y agregar valores incorrectos empeoraría CLS.
- **Impacto SEO estimado:** Bajo-Medio (Core Web Vitals).
