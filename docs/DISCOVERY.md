# Bitácora de Descubrimientos y Decisiones Técnicas (DISCOVERY.md)

Este documento sirve como registro centralizado para dudas, hallazgos técnicos, ambigüedades arquitectónicas e inconsistencias encontradas por los agentes de IA y desarrolladores en el repositorio de **www-datamaq**.

---

## 1. Protocolo de Registro

Cada vez que un agente o desarrollador identifique un comportamiento inesperado, una duda sobre lógica de negocio, o tome una decisión arquitectónica clave, debe registrarla en la sección correspondiente utilizando el siguiente formato:

### Estructura de Entrada:
```markdown
### [ID-DISCOVERY] Título Descriptivo del Hallazgo
* **Fecha:** AAAA-MM-DD
* **Estado:** [Abierto | Resuelto | Mitigado]
* **Impacto:** [Alto | Medio | Bajo]
* **Componentes afectados:** [Ruta del archivo o módulo]
* **Descripción:** Detalle de la inconsistencia o duda encontrada.
* **Resolución / Decisión:** Acción tomada o respuesta del desarrollador principal.
```

---

## 2. Historial de Descubrimientos y Decisiones

### [DISC-001] Divergencia en el tag Robots de Lecciones de Cursos
* **Fecha:** 2026-06-27
* **Estado:** Resuelto
* **Impacto:** Alto
* **Componentes afectados:** [head.html](file:///home/agustin/proyectos_software/www-datamaq/templates/partials/head.html) y [lesson.html](file:///home/agustin/proyectos_software/www-datamaq/templates/cursos/lesson.html)
* **Descripción:** La ruta `vista_leccion` definía en el backend `"meta_robots": "noindex, follow"` para evitar la indexación de lecciones individuales del catálogo. Sin embargo, el template `lesson.html` llamaba a la macro de cabecera sin pasar el parámetro robots, causando que se renderizara el valor por defecto `"index,follow"`.
* **Resolución / Decisión:** Se modificó la macro de cabecera en `head.html` para priorizar dinámicamente `seo_data.meta_robots` si este es enviado en el contexto por el servidor: `{{ seo_data.meta_robots or robots }}`.

### [DISC-002] Pérdida de Query Parameters (UTM Tracking) en Redirección Canónica
* **Fecha:** 2026-06-27
* **Estado:** Resuelto
* **Impacto:** Alto/Medio
* **Componentes afectados:** [middleware.py](file:///home/agustin/proyectos_software/www-datamaq/src/infrastructure/fastapi/middleware.py)
* **Descripción:** El middleware encargado de normalizar las URLs (HTTPS, remover www, quitar trailing slashes) reconstruía la URL final canónica utilizando `urlunsplit` con un query string vacío. Esto provocaba que cualquier usuario que accediera con parámetros UTM o identificadores de campaña perdiera el tracking en la redirección.
* **Resolución / Decisión:** Se modificó la construcción de la URL canónica en el middleware para inyectar `request.url.query` en la tupla de `urlunsplit`.

### [DISC-003] Comportamiento del CTA Secundario en el Hero de Inicio
* **Fecha:** 2026-06-27
* **Estado:** Abierto
* **Impacto:** Bajo
* **Componentes afectados:** [contenido.yaml](file:///home/agustin/proyectos_software/www-datamaq/data/contenido.yaml) y [hero.html](file:///home/agustin/proyectos_software/www-datamaq/templates/partials/components/hero.html)
* **Descripción:** El archivo `contenido.yaml` expone un botón CTA secundario (`secondaryCta`) para el componente Hero, pero el template `hero.html` solo renderiza el botón primario. Esto deja el parámetro configurado sin uso visual en el frontend.
* **Resolución / Decisión:** Pendiente de corregir en el template Jinja2 del Hero para habilitar la renderización condicional del botón de acción secundario.

### [DISC-004] Decisión Estratégica: No indexación de lecciones de cursos
* **Fecha:** 2026-06-27
* **Estado:** Resuelto
* **Impacto:** Medio
* **Componentes afectados:** [course_routes.py](file:///home/agustin/proyectos_software/www-datamaq/src/infrastructure/fastapi/routes/course_routes.py) y [main_routes.py](file:///home/agustin/proyectos_software/www-datamaq/src/infrastructure/fastapi/routes/main_routes.py)
* **Descripción:** Se evaluó la conveniencia de indexar las lecciones individuales para captar tráfico técnico. El objetivo comercial de la web no es ser una plataforma de cursos de programación, sino un canal de generación de leads B2B calificados de servicios de IoT y monitoreo de energía en plantas. Indexar lecciones de código atraería tráfico con intencionalidad no comercial (desarrolladores/estudiantes) y diluiría la conversión.
* **Resolución / Decisión:** Se descarta la indexación de lecciones individuales. Se mantiene `"noindex, follow"` para lecciones y quizzes. Únicamente se indexan la página general de cursos y los temarios de cursos como prueba de topic authority y E-E-A-T.

### [DISC-005] Estructura semántica de encabezados en el perfil de instructor
* **Fecha:** 2026-06-27
* **Estado:** Resuelto
* **Impacto:** Bajo
* **Componentes afectados:** [instructor.html](file:///home/agustin/proyectos_software/www-datamaq/templates/cursos/instructor.html)
* **Descripción:** El H1 de la página de instructor era genérico ("Perfil del Instructor") y el nombre propio del profesional estaba en H2, reduciendo la relevancia del SEO semántico para búsquedas de marca personal de autores/instructores.
* **Resolución / Decisión:** Se cambió el H1 principal a `Instructor: {{ instructor.name }}` y el H2 interno que duplicaba el nombre se degradó a un elemento `<p>` con la misma clase CSS para conservar el diseño.

### [DISC-006] Forzar BASE_URL en canonical_url para estabilidad de proxies
* **Fecha:** 2026-06-27
* **Estado:** Resuelto
* **Impacto:** Medio
* **Componentes afectados:** [seo.py](file:///home/agustin/proyectos_software/www-datamaq/src/infrastructure/fastapi/utils/seo.py) y [config.py](file:///home/agustin/proyectos_software/www-datamaq/src/infrastructure/settings/config.py)
* **Descripción:** El helper `canonical_url` generaba URLs relativas/absolutas dinámicamente usando el host del request. Si el proxy en producción está mal configurado, esto inyectaba canonicals de `localhost` o IPs internas.
* **Resolución / Decisión:** Se añadió `BASE_URL` a la configuración (`https://datamaq.com.ar` como fallback) y se modificó `canonical_url` para forzar el esquema y netloc provistos por esta base URL en lugar de los dinámicos. Los tests de aserción canónica en `test_seo.py` también se ajustaron.

### [DISC-007] Optimización de textos descriptivos alternativos (alt) para fotos
* **Fecha:** 2026-06-27
* **Estado:** Resuelto
* **Impacto:** Bajo
* **Componentes afectados:** [contenido.yaml](file:///home/agustin/proyectos_software/www-datamaq/data/contenido.yaml)
* **Descripción:** Las fotos asociadas al técnico utilizaban textos descriptivos alternativos genéricos como `"Foto del técnico a cargo"` y `"Técnico a cargo de la implementación"`. Esto representaba una oportunidad perdida para inyectar semántica de marca y accesibilidad de cara al algoritmo de búsqueda de imágenes de Google.
* **Resolución / Decisión:** Se modificaron los valores de `alt` en `contenido.yaml` para incluir el nombre del técnico y la especialidad: `"Foto de Agustin Bustos, técnico a cargo en DataMaq"` y `"Agustin Bustos, técnico a cargo de la implementación de equipos IoT"`.

---

## 3. Decisiones de Arquitectura Consolidadas

* **SSR con Jinja2:** El proyecto realiza server-side rendering puro para todo el contenido indexable. Las interacciones dinámicas en cliente se resuelven mediante módulos de Javascript vanilla independientes montados en el frontend, evitando frameworks SPA complejos y maximizando el rendimiento SEO.
* **Normalización Estricta de URLs (308):** Se utiliza redirección HTTP 308 (Permanent Redirect) para normalizar el tráfico de manera consistente hacia el host canónico sin www y sin trailing slash, manteniendo el método de solicitud original.
* **Desacoplamiento de Datos de Contenido:** Está prohibido hardcodear textos promocionales, descripciones técnicas de servicios o datos de cursos directamente en los templates HTML o en los endpoints de FastAPI. Todo el contenido dinámico del negocio debe residir en `data/` en archivos YAML o Markdown.
