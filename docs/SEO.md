# Auditoría SEO Técnico On-Page - www-datamaq

Este documento contiene los resultados de la auditoría SEO técnica realizada sobre el código fuente del proyecto **DataMaq** (migrado de Vue SPA a FastAPI + Jinja2 SSR).

---

## 1. Hallazgos Críticos (Bloqueantes para Indexación)

### 1.1 Directiva `noindex` no aplicada en las lecciones de los cursos
* **Archivo:** [course_routes.py](file:///home/agustin/proyectos_software/www-datamaq/src/infrastructure/fastapi/routes/course_routes.py#L150) y [lesson.html](file:///home/agustin/proyectos_software/www-datamaq/templates/cursos/lesson.html#L9)
* **Severidad:** Alta
* **Problema:** La ruta `vista_leccion` define en su diccionario de SEO `"meta_robots": "noindex, follow"`. Sin embargo, el template `lesson.html` llama a la macro `head_seo` sin pasarle explícitamente el parámetro `robots`, por lo que se inyecta el valor por defecto `"index,follow"`. Esto causará la indexación no deseada de las lecciones individuales y cuestionarios por parte de los buscadores.
* **Sugerencia de Solución (Jinja2):**
  En [lesson.html](file:///home/agustin/proyectos_software/www-datamaq/templates/cursos/lesson.html#L9), modificar la llamada a la macro:
  ```html
  {{ seo_macro.head_seo(request=request, seo_data=seo, brand=brand, robots=seo.meta_robots or 'index,follow') }}
  ```

### 1.2 Pérdida de Query Params en redirecciones del middleware canónico
* **Archivo:** [middleware.py](file:///home/agustin/proyectos_software/www-datamaq/src/infrastructure/fastapi/middleware.py#L58)
* **Severidad:** Alta/Media
* **Problema:** Cuando el middleware de redirección canónica detecta la necesidad de redirigir (de `www` a sin `www`, o de HTTP a HTTPS), reconstruye la URL destino utilizando `urlunsplit((scheme, host, path, "", ""))` descartando completamente la query string original. Esto destruye parámetros de analítica y marketing esenciales (ej: `?utm_source=...`) en el primer contacto del usuario.
* **Sugerencia de Solución (Python/FastAPI):**
  En [middleware.py](file:///home/agustin/proyectos_software/www-datamaq/src/infrastructure/fastapi/middleware.py#L57-L60):
  ```python
      if needs_redirect:
          # Conservar los query parameters originales para no perder el tracking UTM
          canonical = urlunsplit((scheme, host, path, request.url.query, ""))
          return RedirectResponse(url=canonical, status_code=308)
  ```

---

## 2. Advertencias (Mejoras Recomendadas)

### 2.1 Falta de configuración de `manifest.json` para PWA básico
* **Archivo:** [head.html](file:///home/agustin/proyectos_software/www-datamaq/templates/partials/head.html#L3) y [static/](file:///home/agustin/proyectos_software/www-datamaq/static)
* **Severidad:** Media
* **Problema:** El proyecto no dispone de un archivo `manifest.json` referenciado en la cabecera de las páginas. Esto afecta el SEO móvil e impide que motores de búsqueda reconozcan la capacidad instalable de la aplicación.
* **Sugerencia de Solución (Código propuesto):**
  1. Crear el archivo `static/manifest.json` con el siguiente contenido:
     ```json
     {
       "short_name": "DataMaq",
       "name": "DataMaq - Monitoreo de Energía e IoT Industrial",
       "icons": [
         {
           "src": "/static/favicon.svg",
           "type": "image/svg+xml",
           "sizes": "any"
         }
       ],
       "start_url": "/",
       "background_color": "#0d0e12",
       "theme_color": "#00f0ff",
       "display": "standalone",
       "orientation": "portrait"
     }
     ```
  2. En [head.html](file:///home/agustin/proyectos_software/www-datamaq/templates/partials/head.html#L3-L4), enlazar el manifest:
     ```html
     <link rel="manifest" href="{{ request.url_for('static', path='manifest.json') }}">
     ```

### 2.2 Exclusión de perfiles de instructores en `sitemap.xml`
* **Archivo:** [main_routes.py](file:///home/agustin/proyectos_software/www-datamaq/src/infrastructure/fastapi/routes/main_routes.py#L53)
* **Severidad:** Media/Baja
* **Problema:** El sitemap dinámico agrega las páginas de inicio, contacto, términos, localidades, industrias y cursos, pero omite los perfiles de los instructores. Bajo la directriz E-E-A-T de Google, indexar las páginas biográficas de los autores del contenido es una práctica recomendada.
* **Sugerencia de Solución (Python/FastAPI):**
  En [main_routes.py](file:///home/agustin/proyectos_software/www-datamaq/src/infrastructure/fastapi/routes/main_routes.py#L60-L61), agregar el bucle para incorporar los perfiles de instructores:
  ```python
      for instructor_id in cursos_service.get_instructores_dict().keys():
          urls.append({
              "loc": f"{base_url}/cursos/instructor/{instructor_id}",
              "lastmod": lastmod,
              "changefreq": "monthly",
              "priority": "0.5",
          })
  ```

### 2.3 Estructura débil de encabezados en la página del instructor
* **Archivo:** [instructor.html](file:///home/agustin/proyectos_software/www-datamaq/templates/cursos/instructor.html#L34-L38)
* **Severidad:** Media/Baja
* **Problema:** El único `H1` de la página es `"Perfil del Instructor"`. El nombre real del instructor se encuentra dentro de un tag `H2`. Semánticamente, el `H1` debería representar el tema principal de la página, es decir, el nombre del instructor.
* **Sugerencia de Solución (Jinja2):**
  En [instructor.html](file:///home/agustin/proyectos_software/www-datamaq/templates/cursos/instructor.html#L34-L38), cambiar el H1 al nombre del instructor y quitar/modificar el subtítulo:
  ```html
  <!-- Línea 34 -->
  <h1 class="c-curso-section__title">Instructor: {{ instructor.name }}</h1>
  <div class="c-instructor-perfil">
      <img src="{{ instructor.photo }}" alt="{{ instructor.name }}" class="c-instructor-perfil__photo">
      <div class="c-instructor-perfil__info">
          <!-- Modificar Línea 38 a un elemento de párrafo descriptivo o degradar a h2 -->
          <p class="c-instructor-perfil__role" style="font-size: 1.25rem; font-weight: 600;">{{ instructor.role }}</p>
  ```

### 2.4 Helper de URL canónica vulnerable en entornos proxy
* **Archivo:** [seo.py](file:///home/agustin/proyectos_software/www-datamaq/src/infrastructure/fastapi/utils/seo.py#L5)
* **Severidad:** Media/Baja
* **Problema:** La función `canonical_url` reconstruye la URL utilizando `request.url` que obtiene el netloc dinámicamente del framework. Si el balanceador de carga o reverse proxy en producción no reenvía correctamente las cabeceras `Host` o `X-Forwarded-Host`, se inyectarán canonicals apuntando a `localhost:8000` o a la IP privada del contenedor en producción.
* **Sugerencia de Solución (Python):**
  Utilizar una constante configurable en `config` o inyectar una base URL explícita para producción:
  ```python
  def canonical_url(request_url: Any, force_https: bool = True, strip_query: bool = True, base_url: str = "https://datamaq.com.ar") -> str:
      url = str(request_url)
      scheme, netloc, path, query, fragment = urlsplit(url)
      if base_url:
          b_scheme, b_netloc, _, _, _ = urlsplit(base_url)
          scheme = b_scheme
          netloc = b_netloc
      else:
          if force_https:
              scheme = "https"
      if strip_query:
          query = ""
      return urlunsplit((scheme, netloc, path, query, fragment))
  ```

### 2.5 Textos descriptivos alternativos (Alt) genéricos en datos
* **Archivo:** [contenido.yaml](file:///home/agustin/proyectos_software/www-datamaq/data/contenido.yaml#L9)
* **Severidad:** Baja
* **Problema:** Las imágenes asociadas al técnico a cargo utilizan valores de `alt` genéricos como `"Foto del técnico a cargo"` y `"Técnico a cargo de la implementación"`.
* **Sugerencia de Solución (YAML):**
  Modificar el archivo [contenido.yaml](file:///home/agustin/proyectos_software/www-datamaq/data/contenido.yaml#L9):
  ```yaml
  brand:
    technician:
      photo:
        alt: "Foto de Agustin Bustos, Técnico Universitario a cargo en DataMaq"
  ```

### 2.6 CTA Secundario inactivo en el Hero de la página de inicio
* **Archivo:** [hero.html](file:///home/agustin/proyectos_software/www-datamaq/templates/partials/components/hero.html#L11) y [contenido.yaml](file:///home/agustin/proyectos_software/www-datamaq/data/contenido.yaml#L67)
* **Severidad:** Baja
* **Problema:** En el archivo de configuración `contenido.yaml` se provee una acción secundaria para el Hero: `secondaryCta: href: '#servicios', label: "Ver alcance técnico"`. Sin embargo, en el template de Jinja2 `hero.html` solo se dibuja el botón primario, impidiendo que el usuario use este atajo de navegación interna.
* **Sugerencia de Solución (Jinja2):**
  En [hero.html](file:///home/agustin/proyectos_software/www-datamaq/templates/partials/components/hero.html#L11-L13):
  ```html
  <div data-v-236fef00="" class="c-home-hero__actions" style="display: flex; gap: 1rem; flex-wrap: wrap;">
      <a data-v-236fef00="" class="tw:btn-primary c-home-hero__primary" href="{{ data.primaryCta.href }}" target="_blank" rel="noopener noreferrer">{{ data.primaryCta.label }}</a>
      {% if data.secondaryCta %}
      <a data-v-236fef00="" class="tw:btn-outline c-home-hero__secondary" href="{{ data.secondaryCta.href }}">{{ data.secondaryCta.label }}</a>
      {% endif %}
  </div>
  ```

### 2.7 Falta de Datos Estructurados Schema.org específicos (FAQPage y Person)
* **Archivo:** [head.html](file:///home/agustin/proyectos_software/www-datamaq/templates/partials/head.html) e [instructor.html](file:///home/agustin/proyectos_software/www-datamaq/templates/cursos/instructor.html)
* **Severidad:** Baja
* **Problema:** Aunque la página de inicio cuenta con una sección de FAQ, no tiene marcado JSON-LD de `FAQPage`. Del mismo modo, el perfil del instructor carece de un Schema `Person` enriquecido.
* **Sugerencia de Solución (JSON-LD):**
  Agregar condicionalmente bloques JSON-LD en los templates cuando corresponda, o extender la estructura `@graph` del macro `head_seo`.

---

## 3. Buenas Prácticas Ya Implementadas (Fortalezas)

1. **Meta Viewport centralizado:** Correctamente inyectado en la macro `head_seo` de [head.html](file:///home/agustin/proyectos_software/www-datamaq/templates/partials/head.html#L4).
2. **Redirección Canónica a nivel de Middleware:** Normaliza HTTPS, no-www, y remueve trailing slashes usando la redirección recomendada HTTP 308 en [middleware.py](file:///home/agustin/proyectos_software/www-datamaq/src/infrastructure/fastapi/middleware.py).
3. **Encabezado H1 único por página:** Respetado en todas las páginas indexables de la web.
4. **Imágenes con atributos Alt configurados:** Todas las etiquetas `<img>` mapeadas utilizan de forma dinámica textos alternativos bien provistos.
5. **Rutas amigables:** FastAPI no expone parámetros de consulta ni mayúsculas en las rutas indexables.
6. **Manejo correcto de indexación en errores:** Las páginas de error HTTP 404 reciben la etiqueta `noindex,follow` de forma dinámica.
7. **Marcado Schema.org para cursos:** Excelente implementación de los esquemas `Course` y `CourseInstance` en [detail.html](file:///home/agustin/proyectos_software/www-datamaq/templates/cursos/detail.html#L172-L195).
8. **Sitemap dinámico y robots.txt:** Correctamente provistos y enlazados mutuamente.
