# Arquitectura e Implementación de Cursos - Datamaq

Este documento detalla la auditoría, el análisis y el diseño técnico para la incorporación de una sección de capacitación/cursos bajo la ruta `/cursos` en el ecosistema **Datamaq**. El diseño se inspira en la estructura del popular LMS **LearnPress** (WordPress), adaptada a la arquitectura **SSR (Server-Side Rendering)** del proyecto, basada en **FastAPI + Jinja2 + YAML** y siguiendo principios de **Clean Architecture / DDD**.

---

## 1. Auditoría y Objetivos

### 1.1 Objetivos de la Sección Cursos
- **SSR Completo (SEO-First):** Todo el contenido de los cursos, planes de estudio y lecciones teóricas debe renderizarse en el HTML inicial.
- **Acceso Público y Abierto:** Todo el catálogo y las lecciones individuales serán de acceso libre, eliminando la necesidad de sistemas de autenticación, registro de usuarios o base de datos en el servidor para control de accesos.
- **Estructura LearnPress:** Organizar el contenido de capacitación en Cursos (Courses), Secciones (Sections), Lecciones (Lessons) y opcionalmente Cuestionarios (Quizzes).
- **SEO y Rich Cards:** Generar marcado estructurado tipo `Course` de Schema.org en JSON-LD para indexación y visualización rica en motores de búsqueda.
- **Fidelidad y UX Premium:** Ofrecer un reproductor de cursos fluido con acordeones interactivos y soporte de lecciones en video/texto, utilizando *Progressive Enhancement* mediante ES Modules nativos y CSS puro.

### 1.2 Estado de Integración en el Proyecto Actual
- **Rutas Existentes:** `/`, `/contact`, `/industria/{industria}.html`, `/{provincia}/{municipio}/{localidad}.html`.
- **Acceso a Datos:** Centralizado en `DataService` a través de archivos YAML en `data/`.
- **CSS / Estilos:** Nativos en `static/css/`, sin preprocesadores. Los cursos requerirán `cursos.css` específico.
- **JS / Interactividad:** Modular en `static/js/modules/`. Los cursos requerirán un gestor interactivo `CourseManager.js` para persistencia en el navegador (`localStorage`) de las lecciones completadas, lo cual es la solución definitiva de seguimiento al no requerir inicio de sesión.

---

## 2. Modelado de Datos (YAML & Pydantic)

Se propone almacenar la base de datos de cursos en un archivo separado: `data/cursos.yaml`. Esto evita congestionar `contenido.yaml` y mantiene limpia la separación de dominios de negocio.

### 2.1 Estructura Propuesta para `data/cursos.yaml`
```yaml
cursos:
  - id: "curso-python-iot-industrial"
    slug: "python-iot-industrial"
    title: "Python e IoT para el Monitoreo Industrial"
    description_short: "Aprende a capturar variables operativas en tiempo real utilizando Python, microcontroladores y protocolos de comunicación industrial."
    description_long: "Este curso práctico cubre la arquitectura completa de una solución IoT industrial, desde la lectura de sensores de energía y estados de máquina hasta la persistencia y visualización en dashboards..."
    duration: "24 horas de cursada"
    level: "Intermedio"
    language: "Español"
    price: 0 # 0 para gratis, o valor numérico
    og_image: "/static/media/cursos/og-python-iot.webp"
    instructor:
      name: "Agustin Bustos"
      role: "Técnico en Captura de Datos & Programador"
      photo: "/static/media/tecnico-a-cargo.webp"
      bio: "Especialista en captura automática de datos operativos e integración de sistemas industriales con Python."
    sections:
      - id: "sec-introduccion"
        title: "Módulo 1: Introducción a la Captura de Datos"
        description: "Fundamentos de la adquisición de señales analógicas y digitales en planta."
        items:
          - type: "lesson"
            id: "les-bienvenida"
            slug: "bienvenida-y-conceptos"
            title: "Bienvenida y Conceptos de IoT Industrial"
            duration: "15 min"
            content_type: "markdown" # markdown o video
            video_url: "https://www.youtube.com/embed/dQw4w9WgXcQ"
            content: |
              ### Introducción al curso
              Bienvenidos al curso de **Python e IoT para la Industria**. En esta lección inicial veremos:
              - Qué es la captura automática de datos operativos.
              - Diferencias entre IT y OT.
              - El rol de los protocolos como Modbus y MQTT.
          - type: "lesson"
            id: "les-entorno-desarrollo"
            slug: "configuracion-entorno-desarrollo"
            title: "Configuración del Entorno de Desarrollo"
            duration: "20 min"
            content_type: "markdown"
            content: |
              ### Instalación de herramientas
              Para comenzar necesitaremos configurar nuestro entorno local con:
              1. **Python 3.12** o superior.
              2. Un editor de código como **VS Code**.
              3. Creación y activación de un entorno virtual (`venv`).
      - id: "sec-protocolos-comunicacion"
        title: "Módulo 2: Protocolos de Comunicación Industrial"
        description: "Estudio e implementación práctica de protocolos de enlace de datos."
        items:
          - type: "lesson"
            id: "les-mqtt-broker"
            slug: "protocolo-mqtt-y-brokers"
            title: "Protocolo MQTT y Configuración de Broker"
            duration: "30 min"
            content_type: "video"
            video_url: "https://www.youtube.com/embed/dQw4w9WgXcQ"
            content: "En este video tutorial realizaremos la configuración paso a paso de un broker MQTT (Mosquitto) y probaremos publicaciones/suscripciones básicas desde Python."
```

### 2.2 Nuevos Modelos Pydantic en `src/domain/models.py`
Para asegurar la validación **Fail-Fast** en la carga de los cursos, implementaremos los siguientes esquemas de validación:

```python
# --- Modelos de Cursos (LMS) ---
class InstructorModel(BaseModel):
    name: str
    role: str
    photo: str
    bio: str

class LessonModel(BaseModel):
    type: str = "lesson"
    id: str
    slug: str
    title: str
    duration: str
    content_type: str  # "markdown" | "video"
    video_url: Optional[str] = None
    content: str

class CourseSectionModel(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    items: List[LessonModel]

class CourseModel(BaseModel):
    id: str
    slug: str
    title: str
    description_short: str
    description_long: str
    duration: str
    level: str
    language: str
    price: float
    og_image: Optional[str] = None
    instructor: InstructorModel
    sections: List[CourseSectionModel]

class CursosContainerModel(BaseModel):
    cursos: List[CourseModel]
```

---

## 3. Capa de Aplicación (`DataService`)

Modificaremos `src/application/data_service.py` para cargar, estructurar y validar los cursos. Deberá implementar el patrón Repository y lectura con caché para optimizar el rendimiento.

```python
# Modificación teórica en src/application/data_service.py
class DataService:
    def __init__(self, content_path: str, geography_path: str, industry_path: str, courses_path: str):
        self.content_path = content_path
        self.geography_path = geography_path
        self.industry_path = industry_path
        self.courses_path = courses_path
        self._cached_cursos: Optional[CursosContainerModel] = None

    def get_cursos_container(self) -> CursosContainerModel:
        if self._cached_cursos is None:
            with open(self.courses_path, "r", encoding="utf-8") as f:
                raw_data: Dict[str, Any] = yaml.safe_load(f) or {"cursos": []}
                self._cached_cursos = CursosContainerModel(**raw_data)
        return self._cached_cursos

    def get_cursos(self) -> List[CourseModel]:
        return self.get_cursos_container().cursos

    def get_curso_por_slug(self, slug: str) -> Optional[CourseModel]:
        for curso in self.get_cursos():
            if curso.slug == slug:
                return curso
        return None

    def get_leccion(self, curso_slug: str, leccion_slug: str) -> Optional[tuple[CourseModel, LessonModel]]:
        curso = self.get_curso_por_slug(curso_slug)
        if not curso:
            return None
        for seccion in curso.sections:
            for item in seccion.items:
                if item.slug == leccion_slug:
                    return curso, item
        return None
```

---

## 4. Capa de Infraestructura (FastAPI & Jinja2)

### 4.1 Rutas de FastAPI (`src/infrastructure/fastapi/routes/course_routes.py`)
Implementaremos un router de cursos para manejar los tres niveles de vista requeridos: el catálogo, la página de detalles del curso (currículum) y la vista interna de la lección.

```python
from fastapi import APIRouter, Request, HTTPException, Depends
from src.infrastructure.fastapi.dependencies import templates, get_contenido, get_chatwoot_token
from src.domain.models import ContenidoModel, CourseModel, LessonModel
from src.infrastructure.fastapi.utils.seo import canonical_url

# Importamos la dependencia de cursos
from src.infrastructure.fastapi.dependencies import get_cursos_service

router = APIRouter(prefix="/cursos", tags=["cursos"])

@router.get("")
async def listado_cursos(
    request: Request,
    contenido: ContenidoModel = Depends(get_contenido),
    cursos_service = Depends(get_cursos_service),
    chatwoot_token: str = Depends(get_chatwoot_token)
):
    cursos = cursos_service.get_cursos()
    brand_data = contenido.brand.model_dump()
    
    seo = {
        "title": "Cursos y Capacitaciones Técnicas | DataMaq",
        "description": "Formación práctica en Python, IoT industrial y captura de datos operativos para ingenieros y técnicos.",
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": contenido.seo.og_image,
    }

    context = {
        "brand": brand_data,
        "content": contenido.content.model_dump(),
        "cursos": [c.model_dump() for c in cursos],
        "seo": seo,
        "chatwoot_token": chatwoot_token,
    }
    return templates.TemplateResponse(request=request, name="cursos/list.html", context=context)


@router.get("/{curso_slug}")
async def detalle_curso(
    request: Request,
    curso_slug: str,
    contenido: ContenidoModel = Depends(get_contenido),
    cursos_service = Depends(get_cursos_service),
    chatwoot_token: str = Depends(get_chatwoot_token)
):
    curso = cursos_service.get_curso_por_slug(curso_slug)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
        
    brand_data = contenido.brand.model_dump()
    seo = {
        "title": f"Curso: {curso.title} | DataMaq",
        "description": curso.description_short,
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": curso.og_image or contenido.seo.og_image,
    }

    context = {
        "brand": brand_data,
        "content": contenido.content.model_dump(),
        "curso": curso.model_dump(),
        "seo": seo,
        "chatwoot_token": chatwoot_token,
    }
    return templates.TemplateResponse(request=request, name="cursos/detail.html", context=context)


@router.get("/{curso_slug}/{leccion_slug}")
async def vista_leccion(
    request: Request,
    curso_slug: str,
    leccion_slug: str,
    contenido: ContenidoModel = Depends(get_contenido),
    cursos_service = Depends(get_cursos_service),
    chatwoot_token: str = Depends(get_chatwoot_token)
):
    resultado = cursos_service.get_leccion(curso_slug, leccion_slug)
    if not resultado:
        raise HTTPException(status_code=404, detail="Lección o curso no encontrado")
        
    curso, leccion = resultado
    brand_data = contenido.brand.model_dump()
    
    # Para el SEO de las lecciones individuales
    seo = {
        "title": f"{leccion.title} - Curso: {curso.title} | DataMaq",
        "description": f"Lección sobre {leccion.title}. Cursado gratuito de DataMaq.",
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": curso.og_image or contenido.seo.og_image,
        # La lección por lo general no queremos que compita directamente con el curso en resultados principales
        "meta_robots": "noindex, follow"  # Evitamos duplicación interna pero permitimos rastreo
    }

    context = {
        "brand": brand_data,
        "content": contenido.content.model_dump(),
        "curso": curso.model_dump(),
        "leccion": leccion.model_dump(),
        "seo": seo,
        "chatwoot_token": chatwoot_token,
    }
    return templates.TemplateResponse(request=request, name="cursos/lesson.html", context=context)
```

### 4.2 Inclusión de las Rutas en FastAPI (`src/infrastructure/fastapi/app.py`)
El router de cursos se incluirá de la siguiente manera:
```python
from src.infrastructure.fastapi.routes import course_routes
# ...
app.include_router(course_routes.router)
```

---

## 5. Diseño Visual y UX (Plantillas & CSS)

### 5.1 Jerarquía de Plantillas Jinja2
Las nuevas plantillas se ubicarán en `src/infrastructure/fastapi/templates/cursos/`:

1. **`list.html`**:
   - Muestra una grilla estilizada de cursos disponibles.
   - Utiliza tarjetas (cards) premium que muestran el título, duración, nivel, instructor y un botón de llamada a la acción (CTA) para ver los detalles del curso.
2. **`detail.html`**:
   - Cabecera del curso con metadatos destacados (duración, cantidad de lecciones, nivel, instructor).
   - Acordeones interactivos de secciones/módulos colapsables que exponen los títulos de las lecciones correspondientes.
   - Enlace directo a la primera lección del curso.
3. **`lesson.html`**:
   - Layout de pantalla completa dividido en dos columnas:
     - **Columna Lateral (Sidebar):** El listado jerárquico de secciones y lecciones del curso actual, indicando el estado activo de la lección en la que se encuentra y botones para marcar como completado.
     - **Área de Contenido Principal:** Renderizador del contenido de la lección (reproductor de video embebido o bloque de texto procesado en markdown) con botones de navegación "Anterior" y "Siguiente".

### 5.2 Estilos CSS (`static/css/cursos.css`)
Implementaremos hojas de estilo con CSS nativo que sigan las convenciones premium del proyecto:
- **Diseño del Acordeón:** Estilizado mediante selectores nativos (`details` y `summary` con transiciones suaves en `max-height` y rotación de flecha).
- **Contenedor del Reproductor:** Layout flexbox responsivo con aspecto de relación `16:9` nativa para los iframes de video.
- **Sidebar de Navegación:** Fijado en pantallas grandes (`position: sticky`), colapsable en pantallas pequeñas (mobile drawer) para una experiencia óptima de aprendizaje en dispositivos móviles.
- **Colores y Estética:** Mantener el tema oscuro/claro armonioso de DataMaq, utilizando variables personalizadas.

### 5.3 Notación Matemática y Técnica en Lecciones

Para mantener la arquitectura **SSR-first** y evitar cargar motores de renderizado matemático en el cliente, las lecciones no utilizan sintaxis LaTeX ni bibliotecas como KaTeX. En su lugar, se emplea:

- **HTML nativo** permitido por el parser Markdown: `<sub>` para subíndices, `<sup>` para superíndices.
- **Caracteres Unicode** para símbolos técnicos: Ω (ohmios), δ (delta), Φ (flujo luminoso), ≤ (menor o igual), × (multiplicación), ² (superíndice dos).

Ejemplos:
- `U<sub>m</sub> = 17.5 kV`
- `tan δ`
- `1 lx = 1 lm/m²`
- `R<sub>pat</sub> × I<sub>Δn</sub> ≤ U<sub>L</sub>`

Esta decisión garantiza que el contenido se renderice completamente en el HTML inicial, sin dependencias de JavaScript adicionales, y respeta los principios de Progressive Enhancement del proyecto. Si en el futuro se requieren fórmulas complejas (integrales, matrices, fracciones apiladas), se evaluará entonces la integración de un motor de renderizado matemático.

---

## 6. Estrategia SEO Técnica

Para alinearse con la rigurosa estrategia de optimización SEO implementada en el proyecto, incorporaremos:

### 6.1 Marcado Schema.org (`Course`)
En la macro `head_seo` de `templates/partials/head.html` (o inyectando un bloque específico en la plantilla de detalle del curso), agregaremos el marcado JSON-LD adecuado:

```json
{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "{{ curso.title }}",
  "description": "{{ curso.description_short }}",
  "provider": {
    "@type": "Organization",
    "name": "{{ brand.brandName }}",
    "sameAs": "{{ seo.canonical_url }}"
  },
  "hasCourseInstance": {
    "@type": "CourseInstance",
    "courseMode": "online",
    "courseWorkload": "PT{{ curso.duration.split(' ')[0] }}H",
    "instructor": {
      "@type": "Person",
      "name": "{{ curso.instructor.name }}",
      "jobTitle": "{{ curso.instructor.role }}",
      "image": "{{ curso.instructor.photo }}"
    }
  }
}
```

### 6.2 Sitemap.xml Dinámico
Modificaremos la función que genera el `sitemap.xml` dinámico en `src/infrastructure/fastapi/routes/main_routes.py` para obtener la lista de cursos del `DataService` y agregarlos automáticamente al XML, asegurando su indexabilidad inmediata:

```python
# Modificación teórica en sitemap.xml
for curso in cursos_service.get_cursos():
    # Añadir URL de detalle del curso
    url_list.append(f"https://datamaq.com.ar/cursos/{curso.slug}")
```

---

## 7. Progressive Enhancement (JavaScript)

Se creará el archivo `static/js/modules/CourseManager.js`. El script modular será opcional; si JS está deshabilitado en el cliente, el estudiante seguirá pudiendo leer las lecciones de texto, ver los videos incrustados y abrir/cerrar acordeones de forma nativa (usando `<details>` de HTML).

### 7.1 Lógica de `CourseManager.js`
- **Persistencia de Progreso:** Guardar en `localStorage` del navegador los IDs de las lecciones completadas (`datamaq_completed_lessons`).
- **Interactividad Visual:**
  - Marcar con un checkbox y una clase `.is-completed` las lecciones finalizadas en el sidebar.
  - Calcular dinámicamente un porcentaje de avance del curso y actualizar una barra de progreso visual en el encabezado.
- **Navegación Fluida:** Manejar clicks en el sidebar para actualizar la lección actual mediante llamadas AJAX opcionales (o recargas de página optimizadas), actualizando dinámicamente el estado del reproductor.

---

## 8. Plan de Pruebas

Se diseñará un conjunto de pruebas unitarias en `tests/test_cursos.py` para validar la integridad y robustez del nuevo módulo:
- **Validación del YAML:** Testear que la carga de `data/cursos.yaml` sea exitosa y que la ausencia de campos obligatorios dispare la excepción esperada en Pydantic.
- **Pruebas de Rutas:**
  - `GET /cursos` devuelve `200 OK` y lista los cursos válidos.
  - `GET /cursos/un-slug-inexistente` devuelve `404 Not Found`.
  - `GET /cursos/python-iot-industrial/leccion-invalida` devuelve `404 Not Found`.
- **Integridad del Sitemap:** Validar que las nuevas rutas dinámicas de los cursos aparezcan correctamente formateadas en el archivo XML devuelto por el endpoint `/sitemap.xml`.
