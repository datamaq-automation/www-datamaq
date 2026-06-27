# www-datamaq

Sitio web y plataforma técnica de **DataMaq**. El sistema presenta las soluciones de instalación de hardware IoT industrial para el monitoreo de energía y captura automática de datos operativos, el alcance de los servicios de asesoramiento en análisis de datos, y ofrece un anexo de capacitación técnica aplicada (LMS).

Construido con **FastAPI** y Python, utilizando una arquitectura hexagonal/limpia y renderizado dinámico mediante plantillas HTML (Jinja2) a partir de datos estructurados en archivos YAML y Markdown.

## Estructura del Proyecto

* **[data/](file:///home/agustin/proyectos_software/www-datamaq/data)**: Contiene los archivos de contenido general, servicios, cobertura, leads y el catálogo de capacitaciones y lecciones (`*.yaml` y `*.md`).
* **[src/](file:///home/agustin/proyectos_software/www-datamaq/src)**: Código fuente de la aplicación organizado en capas de arquitectura limpia:
  * **[domain/](file:///home/agustin/proyectos_software/www-datamaq/src/domain)**: Modelos de datos (Pydantic).
  * **[application/](file:///home/agustin/proyectos_software/www-datamaq/src/application)**: Lógica de negocio y servicios de datos.
  * **[infrastructure/](file:///home/agustin/proyectos_software/www-datamaq/src/infrastructure)**: Inicialización de FastAPI, configuración de rutas web y middleware.
* **[templates/](file:///home/agustin/proyectos_software/www-datamaq/templates)**: Plantillas Jinja2 para la interfaz de usuario.
* **[static/](file:///home/agustin/proyectos_software/www-datamaq/static)**: Archivos estáticos (CSS, JS, imágenes).
* **[tests/](file:///home/agustin/proyectos_software/www-datamaq/tests)**: Conjunto de pruebas unitarias y de integración del sistema.

---

## Inicio Rápido Local

### 1. Requisitos Previos
* **Python 3.12** o superior instalado en el sistema.
* Utilidad `lsof` (habitual en entornos Linux/macOS) para la gestión automática del puerto en modo desarrollo.

### 2. Configuración de Entorno
Copia el archivo de plantilla `.env.example` para crear tu configuración local:
```bash
cp .env.example .env
```
Asegúrate de editar el archivo `.env` recién creado y colocar los valores de configuración requeridos (por ejemplo, tokens e identificadores para servicios integrados).

### 3. Ejecución del Servidor de Desarrollo
El proyecto cuenta con un script de automatización que gestiona la creación del entorno virtual (`venv`), instala las dependencias de [requirements.txt](file:///home/agustin/proyectos_software/www-datamaq/requirements.txt) si es la primera ejecución, y arranca el servidor local con recarga automática:

```bash
./run.sh
```
El servidor estará accesible en: [http://localhost:8000](http://localhost:8000).

---

## Ejecución de Pruebas

Para correr el set de pruebas automatizadas y validar el correcto funcionamiento de las rutas, redirecciones y el catálogo de cursos:

1. Asegúrate de tener el entorno virtual activo:
   ```bash
   source venv/bin/activate
   ```
2. Ejecuta `pytest`:
   ```bash
   pytest
   ```
   *(Opcional) Para correr las pruebas con reporte de cobertura:*
   ```bash
   pytest --cov=src tests/
   ```
