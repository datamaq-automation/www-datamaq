# Especificación de Requisitos de Software (SRS.md)

Este documento define la Especificación de Requisitos de Software (SRS) para la plataforma web de servicios técnicos de **DataMaq**.

---

## 1. Introducción

El sistema es la plataforma web institucional y técnica de **DataMaq**, una firma especializada en la implementación de equipos IoT industriales para el monitoreo de energía y la captura automática de datos operativos (producción, variables críticas de planta, kWh, factor de potencia, etc.). 

El objetivo principal de la plataforma es exponer el alcance de las soluciones de instalación de hardware IoT, presentar los servicios de asesoramiento y análisis de datos para la toma de decisiones, capturar leads/proyectos mediante formularios interactivos y ofrecer una base de conocimiento técnica (catálogo de capacitaciones y lecciones enriquecidas) como un anexo complementario para los equipos de trabajo industriales.

---

## 2. Requerimientos Funcionales

El sistema debe cumplir con los siguientes requerimientos funcionales:

### RF-01: Exposición de Soluciones y Alcance Técnico (Core)
* El sistema debe presentar la propuesta de valor de DataMaq, detallando las soluciones IoT de monitoreo de energía y los servicios de asistencia técnica en análisis de datos.
* Debe estructurar y mostrar la información del proceso de implementación en sitio, tarifas, cobertura geográfica (zonas operativas) y sectores industriales objetivo.

### RF-02: Formulario Interactivo de Contacto y Captura de Leads (Core)
* La plataforma debe contar con un formulario dinámico de contacto en pasos (identidad del cliente, alcance del proyecto/consulta y datos de contacto).
* El sistema debe validar la información requerida de los pasos del formulario y registrar los leads de proyectos en la carpeta [data/leads/](file:///home/agustin/proyectos_software/www-datamaq/data/leads) para su posterior seguimiento.

### RF-03: Catálogo de Capacitaciones Técnicas (Anexo)
* Como complemento educativo, el sistema debe cargar de forma dinámica el catálogo de capacitaciones definido en [data/cursos/](file:///home/agustin/proyectos_software/www-datamaq/data/cursos).
* Cada elemento del catálogo debe mostrar el título de la capacitación, la descripción técnica orientada a equipos industriales, la duración y el instructor.

### RF-04: Renderizado de Lecciones y Base de Conocimiento (Anexo)
* El sistema debe permitir visualizar lecciones técnicas en formato Markdown mediante la URL `/cursos/{curso_slug}/{leccion_slug}`.
* Las lecciones deben renderizarse dinámicamente convirtiendo el Markdown a HTML, soportando explicaciones matemáticas, fragmentos de código de programación, imágenes y videotutoriales.

### RF-05: Cuestionarios Técnicos de Autoevaluación (Anexo)
* El sistema debe soportar cuestionarios interactivos de autoevaluación (de selección múltiple o verdadero/falso) para validar conceptos eléctricos, de mantenimiento o análisis de datos.

### RF-06: Automatización de Sitemap y Control Canónico
* El sistema debe generar en tiempo real el archivo `/sitemap.xml` para indexar las páginas de inicio, sectores industriales específicos, instructores y lecciones.
* Debe aplicar un middleware para redireccionar de forma automática cualquier tráfico que no respete el formato canónico del dominio.

---

## 3. Requerimientos No Funcionales

### RNF-01: Arquitectura Limpia/Hexagonal
* El código fuente de la aplicación en [src/](file:///home/agustin/proyectos_software/www-datamaq/src) debe estructurarse en capas separadas (Dominio, Aplicación, Infraestructura), prohibiendo la escritura de lógica de negocio o acceso a datos en los endpoints del router web.

### RNF-02: Desempeño por Caché en Memoria
* Los archivos estáticos estructurados (`.yaml` y `.md`) deben cargarse en memoria caché durante el arranque de la aplicación para minimizar el I/O en disco y asegurar tiempos de respuesta ágiles.

### RNF-03: Estructura Semántica y Optimización SEO
* Todas las secciones de servicios, cobertura, industrias y cursos deben incorporar etiquetas de metadatos únicas (título, descripción corta, URL canónica, tags Open Graph) para optimizar el posicionamiento en motores de búsqueda.

### RNF-04: Robustez en el Despliegue Continuo
* Las actualizaciones de código en producción deben utilizar el mecanismo de comprobación de salud (health check) mediante peticiones HTTP locales en el VPS, revirtiendo automáticamente al último commit de Git estable ante fallas del servidor.

---

## 4. Suposiciones y Restricciones

### Restricciones (R)
* **R-01 (Persistencia estática):** Toda la información de servicios, textos, cobertura, cursos y contenido general se almacena y administra mediante archivos estáticos estructurados en el directorio [data/](file:///home/agustin/proyectos_software/www-datamaq/data).
* **R-02 (Infraestructura de Desarrollo):** El backend debe correr bajo Python 3.12+ utilizando FastAPI, Pydantic, Jinja2 y Uvicorn.
* **R-03 (Despliegue de Seguridad):** El despliegue de la aplicación en el servidor debe ejecutarse bajo un usuario de sistema dedicado en el VPS con permisos acotados que no involucren accesos root por SSH.

### Suposiciones (S)
* **S-01:** Se asume que el cliente final cuenta con navegadores web modernos con soporte estándar para hojas de estilo CSS y componentes de JavaScript asíncronos para interactuar con los cuestionarios y el formulario en pasos.
