# Datamaq - Guía para Agentes de Código

> Documento orientado a agentes de IA. Resume la arquitectura, convenciones, comandos y procesos del proyecto tal como están implementados actualmente. El proyecto utiliza español como idioma principal para contenido, documentación y comentarios de código.

## 1. Resumen del Proyecto

**Datamaq** es la migración de una aplicación de página única (**Vue SPA**) a una aplicación con **Server-Side Rendering (SSR)** usando **FastAPI + Jinja2**. El objetivo principal es mejorar el SEO, los Core Web Vitals y la indexación de motores de búsqueda, manteniendo la fidelidad visual y de UX del diseño legacy.

El sitio es una landing page para servicios técnicos de captura automática de datos operativos (energía eléctrica, producción, variables industriales), asesoramiento técnico y capacitaciones.

Aspectos clave:

- **SSR primario:** el 100% del contenido crítico se renderiza en el HTML inicial.
- **Progressive Enhancement:** JavaScript solo agrega interactividad, nunca es requisito para ver el contenido.
- **Datos centralizados en YAML:** todo el contenido editable vive en `data/*.yaml`.
- **Integración documentada con RASA:** el bot se ejecuta como Action Server en el puerto `5006` (endpoint `/webhook`), aunque en este repositorio actualmente no hay código del bot.

## 2. Stack Tecnológico

- **Lenguaje:** Python 3.12
- **Framework web:** FastAPI 0.137.1
- **Servidor ASGI:** Uvicorn 0.49.0
- **Motor de plantillas:** Jinja2 3.1.6
- **Validación de datos:** Pydantic v2
- **Carga de configuración:** python-dotenv
- **Datos estáticos:** PyYAML
- **Frontend:**
  - HTML semántico generado por Jinja2.
  - CSS nativo (sin preprocesadores ni build de assets en despliegue).
  - JavaScript modular vanilla (ES modules) en `static/js/modules/`.
- **Base de datos:** No hay base de datos relacional aún. Los leads del formulario se guardan como archivos JSON en `data/leads/` (hay un TODO para migrar a PostgreSQL).
- **Entorno virtual:** `venv/` (ignorado por Git).

## 3. Estructura del Proyecto

```text
www-datamaq/
├── data/                       # Contenido editable en YAML
│   ├── contenido.yaml          # Contenido principal de la landing
│   ├── geografia.yaml          # Localidades para páginas SEO locales
│   └── industrias.yaml         # Industrias para páginas SEO por industria
├── docs/                       # Documentación del proyecto
│   ├── architecture.md         # Visión arquitectónica
│   ├── CD.md                   # Guía de despliegue continuo
│   ├── seo_strategy.md         # Estrategia SEO
│   ├── SRS.md                  # Especificación de requisitos
│   ├── TODO.md                 # Tareas pendientes
│   └── TODO.done.md            # Tareas completadas
├── scripts/                    # Scripts operativos
│   ├── deploy-server.sh        # Despliegue remoto por SSH
│   ├── view_logs.sh            # Consulta logs del servicio systemd
│   ├── pre-push.sh             # Hook de calidad previo a push
│   ├── .env.deploy             # Configuración de despliegue (ignorado)
│   └── .env.deploy.example     # Plantilla de configuración de despliegue
├── src/                        # Código fuente
│   ├── domain/                 # Entidades y modelos Pydantic
│   │   └── models.py
│   ├── application/            # Casos de uso y servicios de aplicación
│   │   └── data_service.py
│   ├── adapters/               # Controladores, gateways y presentadores (placeholder)
│   └── infrastructure/         # Frameworks, configuración y detalles técnicos
│       ├── fastapi/            # App FastAPI, rutas, templates y estáticos
│       └── settings/           # Configuración y logger
├── tests/                      # Tests con pytest
├── requirements.txt            # Dependencias Python
├── run.sh                      # Script de desarrollo
├── .env                        # Secretos locales (ignorado)
├── .env.example                # Plantilla de secretos
└── AGENTS.md                   # Este archivo
```

## 4. Arquitectura y Organización del Código

El proyecto sigue una estructura en capas inspirada en Clean Architecture / Ports and Adapters:

### 4.1. Capas

- **`src/domain/`**: Contiene los modelos Pydantic (`models.py`) que representan el contenido, SEO, formulario de contacto y payload de envío. Son la fuente de verdad para la validación de datos.
- **`src/application/`**: Contiene `DataService`, responsable de leer los archivos YAML y devolver objetos validados por Pydantic. Es el único punto de acceso a datos estáticos.
- **`src/adapters/`**: Reservada para controladores, gateways y presentadores. Actualmente contiene archivos `__init__.py` vacíos como placeholders para futura expansión (por ejemplo, integración con CRM o el Action Server de RASA).
- **`src/infrastructure/`**: Aloja la aplicación FastAPI, configuración, logger, templates Jinja2, archivos estáticos y rutas HTTP.

### 4.2. Flujo de Datos

1. FastAPI recibe una request.
2. Las dependencias en `src/infrastructure/fastapi/dependencies.py` inyectan el `DataService`.
3. El servicio lee los YAML correspondientes y los valida con Pydantic.
4. Los datos se pasan como contexto a las plantillas Jinja2.
5. Jinja2 renderiza HTML completo y FastAPI lo devuelve.

### 4.3. Rutas Principales

Definidas en `src/infrastructure/fastapi/routes/`:

- `main_routes.py`:
  - `GET /` - Landing page principal.
  - `GET /robots.txt` - Archivo robots.
  - `GET /sitemap.xml` - Sitemap XML.
  - `GET /dev/preview/{partial_name}` - Preview de partials (desarrollo).
- `seo_routes.py`:
  - `GET /{provincia}/{municipio}/{localidad}.html` - Páginas SEO por localidad.
- `industry_routes.py`:
  - `GET /industria/{industria}.html` - Páginas SEO por industria.
- `contact_routes.py`:
  - `POST /api/v1/contact` - Envío del formulario de contacto (guarda lead en `data/leads/`).

### 4.4. Frontend

- **Templates:** en `src/infrastructure/fastapi/templates/`.
  - `base.html` es el layout base.
  - `index.html` extiende el base y compone la landing con macros.
  - `partials/components/*.html` contiene macros Jinja2 reutilizables (hero, service_card, faq_item, contact_form, etc.).
  - `partials/head.html` contiene la macro `head_seo` que inyecta meta tags, Open Graph, Schema.org y configuración global de JS.
- **Estáticos:** en `src/infrastructure/fastapi/static/`.
  - `css/` - Hojas de estilo nativas.
  - `js/` - Punto de entrada `app.js` y módulos ES en `js/modules/`.
  - `media/` - Imágenes y SVGs.

## 5. Datos y Configuración

### 5.1. Archivos YAML (`data/`)

- `contenido.yaml`: marca, contenido de secciones (hero, servicios, FAQ, about, perfil, legal, contacto) y SEO.
- `geografia.yaml`: jerarquía `localidades > provincia > municipio > localidad-slug` para páginas dinámicas.
- `industrias.yaml`: mapeo `slug -> nombre_industria` para páginas dinámicas.

El `DataService` enriquece automáticamente los CTAs de las tarjetas de servicio a partir de sus títulos.

### 5.2. Variables de Entorno (`.env`)

Ejemplos en `.env.example`:

```text
CHATWOOT_WEBSITE_TOKEN=tu_token_aqui
GOOGLE_ANALYTICS_ID=tu_id_ga
CLARITY_ID=tu_id_clarity
DEBUG=False
CHATWOOT_BASE_URL=https://app.chatwoot.com
```

**Nunca commitear `.env` ni `scripts/.env.deploy`**. Ambos están en `.gitignore`.

### 5.3. Configuración en Código

`src/infrastructure/settings/config.py` carga las variables de entorno y define rutas, título de la app y duración de caché de estáticos.

## 6. Comandos de Build, Ejecución y Tests

### 6.1. Instalación de Dependencias

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> Nota: al momento de redactar esta guía, el entorno virtual del repositorio solo contiene `pip`. Es necesario instalar las dependencias antes de ejecutar o testear.

### 6.2. Ejecutar en Desarrollo

```bash
./run.sh
```

`run.sh` realiza lo siguiente:

1. Mata cualquier proceso en el puerto `8000`.
2. Activa el entorno virtual `venv/bin/activate`.
3. Exporta `PYTHONPATH` para incluir la raíz del proyecto.
4. Ejecuta Uvicorn con recarga automática:

```bash
python3 -m uvicorn src.infrastructure.fastapi.app:app --reload
```

### 6.3. Ejecutar en Producción

El servicio `datamaq.service` ejecuta Uvicorn con el entorno virtual del VPS:

```bash
/var/www/datamaq/.venv/bin/python3 -m uvicorn src.infrastructure.fastapi.app:app --host 0.0.0.0 --port 8000
```

Ver configuración completa del servicio en `docs/CD.md`.

### 6.4. Tests

```bash
export PYTHONPATH=$PYTHONPATH:.
pytest --cov=src --cov-report=term-missing tests/
```

Tests actuales:

- `tests/test_additional_routes.py`: test asíncrono del sitemap con mock del contenido.
- `tests/test_coverage_gap.py`: test de `robots.txt` y comentarios sobre cobertura.

### 6.5. Pre-push Hook

`scripts/pre-push.sh` ejecuta pytest con cobertura y aborta el push si falla. Para usarlo como hook de Git:

```bash
ln -s ../../scripts/pre-push.sh .git/hooks/pre-push
```

## 7. Convenciones de Desarrollo

### 7.1. SSR y HTML-first

- El contenido crítico debe estar en el HTML inicial.
- JavaScript es progresivo: mejora la UX pero no es requisito funcional.
- Las plantillas deben ser semánticas, accesibles y SEO-friendly.

### 7.2. Componentización con Macros Jinja2

- Cada componente reutilizable debe ser una macro en `templates/partials/components/`.
- Las macros deben ser autocontenidas y recibir sus datos por argumentos. Evitar depender del contexto global.
- Ejemplo de macros existentes: `hero.html`, `service_card.html`, `faq_item.html`, `contact_form.html`, `whatsapp_fab.html`, `chatwoot_fab.html`.

### 7.3. Comunicación Jinja2 -> JavaScript

- Usar atributos `data-config-*` o un objeto global inyectado en el `<head>`.
- Ejemplo: `window.APP_CONFIG` en `partials/head.html` expone `gaId`, `clarityId` y `contactApiUrl`.
- Los módulos JS leen elementos del DOM por `data-*` atributos (ver `ChatwootManager.js`).

### 7.4. Estilos

- **CSS nativo**, sin Tailwind ni preprocesadores que requieran compilación en despliegue.
- Cada componente tiene su propia hoja en `static/css/`.
- Aún persisten algunas clases con prefijo `tw:` como remanente de la migración desde Tailwind; el objetivo final es eliminarlas.

### 7.5. Datos

- Todo contenido editable debe ir en `data/*.yaml`, no hardcodeado en templates ni en código Python.
- Los modelos Pydantic en `domain/models.py` validan fail-fast ante datos faltantes.

### 7.6. Idioma

- Contenido, documentación y comentarios: **español**.
- Nombres de variables y funciones: mezcla de inglés técnico y español según el dominio (por ejemplo, `get_contenido`, `ContactSubmitPayload`, `pagina_localidad`). Mantener consistencia con el código existente.

## 8. SEO, Performance y Cache Busting

- **SEO:** SSR, meta tags dinámicos, Open Graph, Twitter Cards, Schema.org JSON-LD, `robots.txt`, `sitemap.xml`.
- **Páginas dinámicas SEO:** rutas por localidad e industria generan títulos y descripciones personalizados.
- **Caché de estáticos:** `CachedStaticFiles` agrega `Cache-Control: public, max-age=604800, immutable` en producción y `no-cache` en desarrollo.
- **Cache busting:** las URLs de estáticos usan `?v=...` o el hash corto de Git en producción, y timestamp en desarrollo. Ver `get_static_version()` en `dependencies.py`.

## 9. Integración con RASA (Documentada)

El proyecto contempla un bot RASA que actúa como **Action Server**:

- Puerto: `5006`
- Endpoint: `/webhook`
- Objetivo: compartir lógica de negocio entre web y bot.

Actualmente no hay implementación del Action Server en este repositorio; la integración está documentada en `docs/architecture.md` y `AGENT.md`.

## 10. Formulario de Contacto y Leads

- El formulario de contacto es un wizard de 3 pasos renderizado server-side.
- La navegación entre pasos y el envío se manejan con `FormManager.js`.
- El endpoint `POST /api/v1/contact` recibe un `ContactSubmitPayload`, genera IDs de trazabilidad y encola la persistencia como tarea en segundo plano (`BackgroundTasks`).
- Los leads se guardan temporalmente como archivos JSON en `data/leads/`.
- **TODO pendiente:** migrar persistencia a PostgreSQL y reenviar a CRM/Google Sheets.

## 11. Despliegue

El despliegue es hacia un VPS propio mediante un flujo de CD documentado en `docs/CD.md`.

### 11.1. Servidor de Producción

- Usuario dedicado sin privilegios: `datamaq`.
- Directorio del proyecto: `/var/www/datamaq`.
- Servicio systemd: `datamaq.service`.
- Logs: `journalctl -u datamaq.service` (también disponible vía `scripts/view_logs.sh`).

### 11.2. Configuración de Despliegue

`scripts/.env.deploy` (no commiteado) debe contener:

```text
DEPLOY_SSH_HOST=
DEPLOY_SSH_PORT=
DEPLOY_SSH_USER=
DEPLOY_REMOTE_DIR=
```

Plantilla disponible en `scripts/.env.deploy.example`.

### 11.3. Flujo Automatizado (GitHub Actions)

> **Estado actual:** el CI se ejecuta localmente a través de `scripts/pre-push.sh`. Existe un workflow de deploy en `.github/workflows/deploy.yml` que se dispara en push a `main`; requiere que los secrets de GitHub (`DEPLOY_SSH_HOST`, `DEPLOY_SSH_PORT`, `DEPLOY_SSH_USER`, `DEPLOY_SSH_KEY`) estén configurados.

El flujo de deploy es:

1. Push a `main` dispara el workflow de GitHub Actions.
2. Se conecta por SSH al VPS usando los secrets `DEPLOY_SSH_HOST`, `DEPLOY_SSH_PORT`, `DEPLOY_SSH_USER` y `DEPLOY_SSH_KEY`.
3. Ejecuta `scripts/deploy-server.sh` en el servidor remoto.
4. El script:
   - Guarda el commit actual para posible rollback.
   - Hace `git pull`.
   - Instala dependencias con `./.venv/bin/pip install -r requirements.txt`.
   - Reinicia el servicio `datamaq.service`.
   - Ejecuta un health-check HTTP a `http://localhost:8000/`.
   - En caso de fallo, revierte al commit anterior y reinicia el servicio.

### 11.4. Scripts Útiles

- `scripts/deploy-server.sh` - Despliegue manual/automatizado.
- `scripts/view_logs.sh` - Ver logs remotos del servicio.
- `scripts/pre-push.sh` - Ejecutar tests antes de push.

## 12. Consideraciones de Seguridad

- **Nunca commitear secretos:** `.env`, `scripts/.env.deploy` y `data/leads/` están en `.gitignore`.
- **Ejecutar la app con usuario no privilegiado** en producción (`datamaq`), nunca como `root`.
- **Validación de datos:** todos los payloads de entrada usan modelos Pydantic.
- **Caché:** estáticos se sirven con caché agresiva en producción; en desarrollo se desactiva.
- **Persistencia de leads:** actualmente los leads se escriben en disco. Asegurar permisos adecuados y planificar migración a base de datos.

## 13. Estado Actual y Notas Importantes

- La migración está en progreso. `docs/TODO.md` lista tareas pendientes como completar la estructura HTML semántica, acondicionar variables CSS, implementar el wizard completo y validar la integración RASA.
- `docs/TODO.done.md` lista lo ya logrado: configuración FastAPI, SSR, modelos YAML, SEO, logger, caché, Chatwoot, .env, tests con cobertura y pre-push hook.
- El repositorio incluye el workflow de deploy `deploy.yml` en `.github/workflows/`; el CI corre localmente mediante `scripts/pre-push.sh`.
- El entorno virtual `venv/` del repositorio ya tiene las dependencias de `requirements.txt` instaladas.
- El hook `pre-push` está activo como symlink a `scripts/pre-push.sh`.

## 14. Referencias Rápidas

- README: `README.md`
- Guía de estilo: `GEMINI.md`
- Arquitectura: `docs/architecture.md`
- Estrategia SEO: `docs/seo_strategy.md`
- Despliegue: `docs/CD.md`
- Requisitos: `docs/SRS.md`
- Pendientes: `docs/TODO.md`
