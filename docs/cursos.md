# Guía Práctica de Cursos y Lecciones en DataMaq

Este documento describe la estructura de datos, el flujo de creación de contenidos y las especificaciones técnicas para dar de alta o modificar cursos, lecciones, cuestionarios e instructores en la plataforma SSR de **DataMaq**.

---

## 1. Estructura de Directorios

Todos los datos de cursos residen de forma estática en la carpeta `data/`. La estructura requerida es la siguiente:

```text
data/
├── instructores.yaml
└── cursos/
    ├── [slug-del-curso-1]/
    │   ├── curso.yaml
    │   └── lecciones/
    │       ├── leccion-1.md
    │       └── leccion-2.md
    └── [slug-del-curso-2]/
        ├── curso.yaml
        └── lecciones/
```

---

## 2. Gestión de Instructores (`data/instructores.yaml`)

Antes de asociar un instructor a un curso, este debe estar registrado en el archivo centralizado `data/instructores.yaml`.

### Formato de `instructores.yaml`:
```yaml
instructores:
  - id: "nombre-apellido"  # ID único que será referenciado desde curso.yaml
    name: "Nombre Completo"
    role: "Título Profesional"
    photo: "/static/media/foto-instructor.webp"  # Ruta a la foto en static
    bio: "Breve biografía del instructor (se recomienda menor a 150 caracteres para SEO)."
    social_links:
      linkedin: "https://www.linkedin.com/in/..."
      github: "https://github.com/..."
      twitter: "https://twitter.com/..."
      website: "https://..."
```

---

## 3. Registro de un Curso (`curso.yaml`)

Cada curso debe tener su propio archivo `curso.yaml` dentro de su carpeta correspondiente en `data/cursos/[slug-del-curso]/`. Este archivo define la estructura del curso, organizada en **Secciones**, **Capítulos** y **Elementos (Lecciones o Quizzes)**.

### Estructura de Campos Obligatorios y Opcionales:

| Campo | Tipo | Descripción | Obligatorio |
| :--- | :--- | :--- | :--- |
| `id` | String | Identificador único del curso (ej: `curso-python-iot`). | Sí |
| `slug` | String | URL amigable del curso (ej: `python-iot`). | Sí |
| `title` | String | Título del curso para SEO y UI. | Sí |
| `description_short` | String | Descripción corta (máximo 80-120 caracteres para meta tag). | Sí |
| `description_long` | String | Descripción larga del curso para el temario principal. | Sí |
| `duration` | String | Duración estimada de cursada (ej: `40 horas de cursada`). | Sí |
| `level` | String | Nivel del curso (ej: `Avanzado`, `Intermedio`, `Introductorio`). | Sí |
| `language` | String | Idioma del dictado (default: `Español`). | No |
| `price` | Float | Costo del curso (default: `0.0` para libre acceso). | No |
| `og_image` | String | Imagen Open Graph. Si se omite, se usa fallback dinámico. | No |
| `instructor_id` | String | ID del instructor registrado en `instructores.yaml`. | Sí |
| `sections` | List | Lista de secciones del temario. | Sí |

### Plantilla de Ejemplo Completo (`curso.yaml`):

```yaml
id: "curso-fastapi-iot"
slug: "fastapi-iot"
title: "Monitoreo Industrial con FastAPI e IoT"
description_short: "Aprendé a capturar y exponer datos de energía y producción en tiempo real."
description_long: "Este curso práctico enseña a estructurar APIs robustas para recibir variables de tableros eléctricos y sensores industriales utilizando FastAPI, Python y comunicación serie Modbus."
duration: "30 horas de cursada"
level: "Intermedio"
instructor_id: "agustin-bustos"
sections:
  - id: "sec-fundamentos"
    title: "Sección A: Fundamentos de API e IoT"
    description: "Configuración inicial de FastAPI e integración con periféricos."
    chapters:
      - id: "chap-cap-1"
        title: "Cap 1: Introducción a la API de Planta"
        description: "Endpoints básicos para recibir cargas de tableros."
        items:
          # Tipo A: Lección de Texto (Markdown local)
          - type: "lesson"
            id: "les-cap-1-1"
            slug: "requisitos-planta"
            title: "1.1 Requisitos de Infraestructura"
            duration: "10 min"
            content_file: "cap-1-1-requisitos-planta.md"

          # Tipo B: Lección de Video (Embebido externo)
          - type: "lesson"
            id: "les-cap-1-2"
            slug: "videotutorial-endpoints"
            title: "1.2 Crear Endpoints para Sensores"
            duration: "25 min"
            content_type: "video"
            video_url: "https://www.youtube.com/embed/dQw4w9WgXcQ"
            content: "En este videotutorial crearemos la API mínima para capturar pulsos de caudalímetros."

          # Tipo C: Cuestionario / Evaluación interactiva
          - type: "quiz"
            id: "quiz-cap-1"
            slug: "evaluacion-conceptos"
            title: "Cuestionario 1: Conceptos Básicos"
            duration: "15 min"
            questions:
              - id: "q1"
                question: "¿Cuál es el puerto por defecto de comunicación Modbus TCP?"
                type: "single_choice"
                options:
                  - "80"
                  - "502"
                  - "8000"
                correct_option: 1  # Índice basado en 0 (la opción correcta es '502')
                explanation: "El protocolo Modbus TCP utiliza de manera estándar el puerto 502."
```

---

## 4. Redacción de Lecciones de Texto (`.md`)

Cuando un elemento en `curso.yaml` se define con `content_file`, el motor de FastAPI buscará un archivo Markdown correspondiente dentro de la carpeta `lecciones/`.

### Lineamientos para escribir el Markdown:
1. **Formato Simple:** No incluyas metadatos frontmatter (YAML al inicio) en el archivo `.md`. FastAPI lee el archivo como texto crudo.
2. **Encabezados:** Inicia el contenido con encabezados de nivel 3 (`###`) o nivel 4 (`####`) para no romper la jerarquía del template principal (donde el título de la lección ya es un `H1`).
3. **Tablas y Código:** Podés utilizar tablas de markdown y bloques de código con sintaxis resaltada (ej: ````python ... ````), ya que el renderizador del backend soporta las extensiones `tables` y `fenced_code`.

### Ejemplo de archivo `.md` (`lecciones/cap-1-1-requisitos-planta.md`):
```markdown
### Requisitos de Conectividad en Planta

Para asegurar la correcta comunicación entre los equipos de medición de energía (Powermeter/Automate) y la API:

1. **Protocolo:** Se debe habilitar el transporte TCP sobre el puerto local.
2. **Dirección IP:** Asignar una IP estática al gateway IoT.

```python
# Ejemplo de payload JSON enviado por el equipo de medición
payload = {
    "device_id": "powermeter-01",
    "kwh_total": 12840.5,
    "active_power_kw": 45.2
}
```
```

---

## 5. Control de Calidad y Validación Técnica

Antes de subir cambios al servidor:
1. **Validación de Tipos (Pydantic):** Levantá el servidor local (`run.sh`) y accedé a `/cursos`. Si hay un error de sintaxis en `curso.yaml` o un tipo de datos no coincide con los modelos del dominio (`src/domain/models.py`), FastAPI generará un error de validación descriptivo al parsear los datos.
2. **Validación de Rutas:** Asegúrate de que todos los campos `slug` e `id` en `curso.yaml` sean únicos dentro del curso y usen únicamente minúsculas y guiones.
3. **Pruebas Automatizadas:** Ejecutá la suite de pruebas del proyecto para validar que no haya problemas de parseo:
   ```bash
   PYTHONPATH=. pytest
   ```
