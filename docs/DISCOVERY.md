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

---

## 3. Decisiones de Arquitectura Consolidadas

* **SSR con Jinja2:** El proyecto realiza server-side rendering puro para todo el contenido indexable. Las interacciones dinámicas en cliente se resuelven mediante módulos de Javascript vanilla independientes montados en el frontend, evitando frameworks SPA complejos y maximizando el rendimiento SEO.
* **Normalización Estricta de URLs (308):** Se utiliza redirección HTTP 308 (Permanent Redirect) para normalizar el tráfico de manera consistente hacia el host canónico sin www y sin trailing slash, manteniendo el método de solicitud original.
* **Desacoplamiento de Datos de Contenido:** Está prohibido hardcodear textos promocionales, descripciones técnicas de servicios o datos de cursos directamente en los templates HTML o en los endpoints de FastAPI. Todo el contenido dinámico del negocio debe residir en `data/` en archivos YAML o Markdown.
