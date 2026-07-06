# Auditoría de Componentes y Responsive (docs/AUDITORIA_COMPONENTES.md)

Este documento detalla la estructura física de los componentes de la interfaz de usuario de **DataMaq**, el estado de su auditoría responsive y usabilidad (Touch Targets) en dispositivos móviles, y las herramientas de telemetría inyectadas en desarrollo.

---

## 1. Mapeo y Estado de la Auditoría

El sistema cuenta con un total de **13 archivos físicos de componentes** en `templates/partials/components/`. Tras la ampliación del enrutador de desarrollo `/dev/preview/*`, **12 componentes son accesibles de forma aislada** para auditoría; el componente `icon.html` es una macro auxiliar de SVG y no requiere previsualización propia.

| Componente | Ruta Física | Previsualización Aislada | Estado | Especificaciones y Correcciones Locales |
| :--- | :--- | :--- | :---: | :--- |
| **Header** | `header.html` | `/dev/preview/header` | **Completado** (✅) | Corregido el bug de especificidad CSS en `.c-home-header__nav` que forzaba el despliegue del menú en móvil. Marca, icono de contacto y CTA ajustados a **44×44 px** como mínimo. Menú hamburguesa visible solo en móvil; menú desktop a partir de `992px`. |
| **Footer** | `footer.html` | `/dev/preview/footer` | **Completado** (✅) | Rediseñado con acordeones nativos en móvil (`<details>` y `<summary>`) con animación y rotación de chevron. El contenido cerrado se oculta mediante `display: none !important`. Restaurada la visibilidad de la marca y datos de contacto en móvil. Altura total móvil reducida de `1140px` a **`700px`**. Todos los controles alcanzan **44×44 px**. |
| **Hero** | `hero.html` | `/dev/preview/hero` | **Completado** (✅) | Sin desbordamientos horizontales ni alertas de Touch Target en viewports `320px`, `375px` y `768px`. La lista de trust-chips utiliza `overflow-x: auto` de forma intencional y controlada; el script de telemetría ignora estos contenedores con scroll programado. |
| **Profile** | `profile.html` | `/dev/preview/profile` | **Completado** (✅) | Sin desbordamientos horizontales ni alertas de Touch Target en viewports `320px`, `375px` y `768px`. Avatar, tarjeta de perfil y grilla de beneficios se adaptan correctamente. |
| **Contact Section** | `contact_section.html` + `contact_form.html` | `/dev/preview/contact_section` | **Completado** (✅) | Stepper triggers, enlace de e-mail alternativo y botón CTA ajustados a **44×44 px**. El stepper se apila en una sola columna en móvil (`max-width: 767.98px`). |
| **Chatwoot FAB** | `chatwoot_fab.html` | `/dev/preview/chatwoot_fab` | **Completado** (✅) | Botón flotante de `3.5rem × 3.5rem` en móvil (**~56px**), bien por encima del mínimo táctil. No requirió ajustes. |
| **Cookie Banner** | `cookie_banner.html` | `/dev/preview/cookie_banner` | **Completado** (✅) | Botones de acción y enlace "Ver más" ajustados a **44×44 px** en todos los viewports. |
| **Dock** | `dock.html` | `/dev/preview/dock` | **Completado** (✅) | Barra de navegación fija inferior. En móvil usa `grid-template-columns: repeat(var(--dock-columns, 4), minmax(3.5rem, 1fr))` y `overflow-x: auto` para soportar hasta 6 ítems sin romper el layout. Todos los enlaces superan **44×44 px**. |
| **FAQ Item** | `faq_item.html` | `/dev/preview/faq_item` | **Completado** (✅) | Acordeón nativo con `<summary>` de padding `1.2rem 1.25rem`; el área táctil supera ampliamente los `44px`. No contiene enlaces internos. No requirió ajustes. |
| **Service Card** | `service_card.html` | `/dev/preview/service_card` | **Completado** (✅) | CTA principal con `min-height: 3.2rem` (**~51px**). Contenido, icono y lista de beneficios se adaptan al ancho móvil. No requirió ajustes. |
| **Section Wrapper** | `section_wrapper.html` | `/dev/preview/section_wrapper` | **Completado** (✅) | Envoltura estructurada de secciones. No introduce elementos interactivos propios; su ancho se controla mediante `tw:container tw:mx-auto tw:px-4`. No requirió ajustes. |
| **Icon** | `icon.html` | *No aplica* | **No aplica** (⚪) | Macro de renderizado de iconos SVG de Bootstrap Icons. Es un helper sin interacción propia; se audita indirectamente dentro de los componentes que lo consume. |

**Resumen:** 12 de 13 componentes auditados, con **0 controles interactivos menores a 44×44 px** y **0 desbordamientos horizontales** no intencionales en viewports `320px`, `375px` y `768px`.

---

## 2. Pautas y Estándares de Usabilidad Móvil (UI/UX)

Para garantizar un producto premium, cada componente auditado y refinado en el repositorio debe cumplir rigurosamente con las siguientes pautas ergonómicas antes de ser considerado estable:

* **Sin desbordamiento horizontal:** El scroll horizontal del cuerpo del documento (`document.body.scrollWidth`) debe ser idéntico al ancho del viewport (`window.innerWidth`) en cualquier resolución móvil (típicamente `320px` a `480px`) y tablet vertical (hasta `768px`). Los contenedores con `overflow-x: auto` o `overflow-x: scroll` intencionales (p. ej., trust-chips del Hero o el dock con muchos ítems) se excluyen del reporte.
* **Touch Targets accesibles (WCAG 2.5.5 / WCAG 2.2):**
  * Todos los controles interactivos (`<a>`, `<button>`, `<input>`, `<select>`, `<textarea>`, `<summary>`) deben poseer un área táctil física de al menos **`44×44 px`**. Esto se logra con `display: inline-flex` o `display: flex`, `align-items: center`, `justify-content: center` y `min-height: 2.75rem` (44 px), sin necesidad de aumentar el tamaño de fuente visual.
  * **CTAs principales a 48×48 px:** Los controles de alta conversión (botón primario `tw:btn-primary`, outline `tw:btn-outline`, CTA del header, icono de contacto móvil del header y botones del banner de cookies) se elevan a **`48×48 px`** (`min-height: 3rem` / `width: 3rem; height: 3rem`), alineándose con el estándar más conservador de Material Design para acciones críticas.
  * Se ignoran del reporte los controles con `pointer-events: none`, `display: none` o `visibility: hidden`, ya que no son interactivos.
* **Contraste de color (WCAG 1.4.3 / WCAG 2.1 AA):**
  * Todo texto debe alcanzar una relación de contraste mínima de **4.5:1** frente a su fondo (3:1 para texto grande).
  * El script utiliza **axe-core** para evaluar el DOM completo bajo la regla `color-contrast` y reporta violaciones con el ratio detectado.
* **Foco visible (WCAG 2.4.7):**
  * Todo control interactivo debe contar con estilos explícitos para `:focus` o `:focus-visible`, garantizando que usuarios de teclado y asistencias puedan percibir el elemento activo.
  * El script inspecciona `document.styleSheets` y verifica que exista al menos una regla que aplique al control.
* **Matriz de viewports:** Toda auditoría se ejecuta como mínimo en `320×568`, `375×667` y `768×1024` para cubrir móvil pequeño, móvil estándar y tablet vertical.
* **Visualización de Marca:** La información de contacto directo (Mail, Dirección) no debe ocultarse en mobile bajo directivas de simplificación, ya que es el motor de conversión directa de leads para la empresa.

---

## 3. Instrumentación de Telemetría en Tiempo Real

Durante la etapa de depuración local, la plataforma cuenta con telemetría integrada de forma global en `templates/base.html` y en `templates/preview.html` importando el script estático modular:
* **Archivo de telemetría:** [static/js/preview-telemetry.js](file:///home/agustin/proyectos_software/www-datamaq/static/js/preview-telemetry.js)

### Funcionalidad de Monitoreo:
1. Limpia automáticamente la consola del navegador (`console.clear()`) tras 1 segundo y ante cada evento de redimensionamiento (`resize`).
2. Imprime un reporte detallado en tiempo real en formato JSON con:
   * Viewport actual (ancho y alto en px).
   * Scroll horizontal total del body (para detectar fugas de responsive).
   * Listado detallado de elementos del DOM que causan desbordamiento horizontal.
   * Análisis automático de Touch Targets indicando la cantidad de controles interactivos menores a `44px` y listando las alertas con su respectivo tamaño físico.
   * Medidas del footer cuando está presente.

### Uso para validar un componente:
```
http://localhost:8000/dev/preview/{nombre_componente}
```

Componentes disponibles en preview: `header`, `footer`, `hero`, `profile`, `contact_section`, `chatwoot_fab`, `cookie_banner`, `dock`, `faq_item`, `service_card`, `section_wrapper`.

---

## 4. Scripts de Auditoría Automatizada

Además de la telemetría en navegador, el repositorio incluye dos scripts de Python para auditar componentes:

### 4.1. Auditoría estructural de previews

* **Archivo:** [scripts/audit_components.py](file:///home/agustin/proyectos_software/www-datamaq/scripts/audit_components.py)

**Qué hace:**
1. Lista los 13 archivos físicos de `templates/partials/components/`.
2. Parsea `templates/preview.html` y detecta cuáles tienen una rama de previsualización aislada.
3. Lanza smoke tests HTTP contra `http://localhost:8000/dev/preview/{componente}`.
4. Si Google Chrome/Chromium está disponible, realiza una verificación headless básica del viewport móvil.

**Uso:**
```bash
# Con el servidor de desarrollo corriendo
python3 scripts/audit_components.py

# Contra otra URL base
python3 scripts/audit_components.py --base-url http://127.0.0.1:5000

# Omitir el chequeo con Chrome
python3 scripts/audit_components.py --skip-chrome
```

### 4.2. Auditoría responsive, táctil y de accesibilidad con Playwright

* **Archivo:** [scripts/audit_responsive.py](file:///home/agustin/proyectos_software/www-datamaq/scripts/audit_responsive.py)
* **Dependencias Python:** [requirements-dev.txt](file:///home/agustin/proyectos_software/www-datamaq/requirements-dev.txt)
* **Dependencias Node:** `axe-core` (instalado en `node_modules/axe-core/axe.min.js`)

**Qué hace:**
1. Abre cada preview en un navegador Chromium headless con cada viewport configurado.
2. Mide `document.body.scrollWidth` y compara con el ancho del viewport.
3. Detecta elementos con desbordamiento horizontal no intencional (ignora contenedores con `overflow-x: auto/scroll` y sus hijos).
4. Detecta controles interactivos (`<a>`, `<button>`, `<input>`, `<select>`, `<textarea>`, `<summary>`) menores a **44×44 px**.
5. Ignora controles no interactivos (`pointer-events: none`, `display: none`, `visibility: hidden`).
6. Ejecuta **axe-core** con una allowlist curada de reglas de accesibilidad:
   * `color-contrast` (WCAG AA).
   * Nombres accesibles: `button-name`, `input-button-name`, `link-name`, `image-alt`, `label`.
   * Estructura: `heading-order`, `landmark-one-main`.
   * ARIA: `aria-required-attr`, `aria-required-children`, `aria-roles`.
   * Identificadores: `duplicate-id`.
   * La regla `region` se excluye deliberadamente porque los previews aislados de componentes no tienen landmarks de página completos.
7. Verifica que cada control interactivo tenga estilos definidos para `:focus` o `:focus-visible`.
8. Reporta la altura del footer cuando el componente la incluye.

**Modo de impacto (`--a11y-warnings`):**
* Por defecto, los hallazgos de accesibilidad adicionales de axe-core **fallan** la auditoría.
* Con `--a11y-warnings` los hallazgos se imprimen como advertencias sin contar como fallas, útil para evaluar el impacto antes de activar el modo estricto.

**Instalación:**
```bash
source venv/bin/activate
pip install -r requirements-dev.txt
playwright install chromium
npm install --save-dev axe-core
```

**Uso:**
```bash
# Con el servidor de desarrollo corriendo (viewports por defecto: 320x568, 375x667, 768x1024)
python3 scripts/audit_responsive.py

# Matriz personalizada de viewports
python3 scripts/audit_responsive.py --viewports 320x568,390x844,768x1024

# Otra URL base
python3 scripts/audit_responsive.py --base-url http://127.0.0.1:5000

# Modo impacto: reporta hallazgos de accesibilidad adicionales sin fallar
python3 scripts/audit_responsive.py --a11y-warnings
```

### 4.3. Auditoría SEO e imágenes con Playwright

* **Archivo:** [scripts/audit_seo.py](file:///home/agustin/proyectos_software/www-datamaq/scripts/audit_seo.py)
* **Dependencias Python:** [requirements-dev.txt](file:///home/agustin/proyectos_software/www-datamaq/requirements-dev.txt)

**Qué hace:**
1. Abre las rutas reales del sitio (`/`, `/contact`, `/cursos`, `/casos`, `/terminos-y-condiciones`) en un navegador Chromium headless.
2. Valida tags HTML y meta tags esenciales:
   * Atributo `lang` en `<html>`.
   * `<title>` no vacío.
   * `<meta name="description">` no vacío.
   * `<link rel="canonical">` con `href` no vacío.
   * Tags Open Graph: `og:title`, `og:description`, `og:image`.
3. Verifica estructura de encabezados: exactamente un `<h1>` y sin saltos inválidos en la jerarquía.
4. Verifica imágenes:
   * Atributo `alt` presente (o marcada como decorativa con `aria-hidden="true"` / `role="presentation"`).
   * Atributos `width` y `height` explícitos para prevenir CLS.

**Modo de impacto (`--seo-warnings`):**
* Por defecto, los hallazgos SEO e imágenes **fallan** la auditoría.
* Con `--seo-warnings` los hallazgos se imprimen como advertencias sin contar como fallas.

**Instalación:**
```bash
source venv/bin/activate
pip install -r requirements-dev.txt
playwright install chromium
```

**Uso:**
```bash
# Con el servidor de desarrollo corriendo
python3 scripts/audit_seo.py

# Otra URL base
python3 scripts/audit_seo.py --base-url http://127.0.0.1:5000

# Modo impacto: reporta hallazgos sin fallar
python3 scripts/audit_seo.py --seo-warnings

# Rutas personalizadas
python3 scripts/audit_seo.py --routes / /contact /cursos
```

### Hallazgos y correcciones recientes

#### Primera corrida con umbral 32 px
Se detectó que el componente **Dock** con 6 enlaces generaba desbordamiento interno en viewport de `375px`. Se corrigió en `static/css/HomePage.css` estableciendo:

* `grid-template-columns: repeat(var(--dock-columns, 4), minmax(3.5rem, 1fr))` en móvil.
* `overflow-x: auto` y `scroll-snap-type: x mandatory` en el dock para scroll horizontal controlado.
* Texto centrado, ajustable a dos líneas y `font-size` reducido en móvil.

#### Segunda corrida con umbral 44×44 px y múltiples viewports
Al subir el estándar a **44×44 px** y auditar `320×568`, `375×667` y `768×1024`, aparecieron fallas reales en:

* **Contact Section / Contact Form:** stepper triggers de `40px` de alto y e-mail alternativo de `37px`.
* **Cookie Banner:** botones de `40px` de alto y enlace "Ver más" de `32px`.
* **Footer:** e-mail de marca de `34px`, términos legales de `33px` y summaries de acordeón en desktop no interactivos.
* **Header:** icono de contacto móvil de `40×40px`.

**Correcciones aplicadas:**
* `static/css/useContactPageActions.css`: stepper triggers y e-mail alternativo a `min-height: 2.75rem`.
* `static/css/CookieBanner.css`: botones y enlace "Ver más" a `min-height: 2.75rem`.
* `static/css/HomePage.css`:
  * Footer: summaries, links de navegación, e-mail de marca y términos legales a `min-height: 2.75rem`.
  * Header: marca, icono de contacto móvil y CTA a `min-height: 2.75rem`.
  * Dock: scroll horizontal controlado para 6 ítems.
* `scripts/audit_responsive.py`: se agregó filtrado de controles con `pointer-events: none` para evitar falsos positivos en summaries de desktop.

Tras las correcciones, la auditoría reporta **0 desbordamientos**, **0 controles menores a 44×44 px**, **0 problemas de contraste** y **0 problemas de foco** en los 13 componentes y 3 viewports.

#### Tercera corrida: contraste de color y foco visible
Se incorporaron dos nuevos chequeos de accesibilidad en `scripts/audit_responsive.py`:

* **Contraste:** se carga `axe-core` desde `node_modules` y se ejecuta la regla `color-contrast` contra el `document.body` de cada preview.
* **Foco visible:** se recorren `document.styleSheets` para detectar reglas que contengan `:focus` o `:focus-visible` y se verifica que apliquen a cada control interactivo.

Resultado: **0 violaciones de contraste** y **0 controles sin estilo de foco** en todos los componentes auditados.

#### Cuarta corrida: allowlist ampliada de accesibilidad
Se expandió el uso de `axe-core` a un subset curado de reglas de accesibilidad (`button-name`, `input-button-name`, `link-name`, `image-alt`, `label`, `heading-order`, `landmark-one-main`, `aria-required-attr`, `aria-required-children`, `aria-roles`, `duplicate-id`).

* Se agregó el flag `--a11y-warnings` para evaluar el impacto sin bloquear el pipeline.
* La primera corrida con allowlist reportó **24 warnings** de la regla `region`, todos provenientes de previews aislados donde no existen landmarks de página completos.
* Se decidió **excluir `region` de la allowlist** porque no refleja un problema real en producción; en las páginas completas los componentes viven dentro de `<main>` y secciones con títulos.

Tras el ajuste, la auditoría en modo estricto reporta **0 desbordamientos**, **0 controles menores a 44×44 px**, **0 problemas de contraste**, **0 problemas de foco** y **0 hallazgos adicionales de accesibilidad** en los 13 componentes y 3 viewports.

#### Quinta corrida: CTAs principales a 48×48 px
Se elevó selectivamente el área táctil de los controles de alta conversión para superar el estándar base de 44×44 px:

* `.tw:btn-primary` y `.tw:btn-outline` en `static/css/src/input.css`: `min-height: 3rem` (48 px).
* Header: icono de contacto móvil y CTA desktop en `static/css/HomePage.css` a `3rem`.
* Cookie banner: botones de acción en `static/css/CookieBanner.css` a `min-height: 3rem`.
* Componentes como Hero, Profile, Contact Form y Service Card ya superaban los 48 px con sus estilos existentes (`3.2rem` / `3.3rem`).

Resultado: la auditoría mantiene **0 fallas** en todos los componentes y viewports, con CTAs principales en el rango óptimo de 48×48 px.

---

## 5. Hook de Pre-push

La auditoría responsive, de accesibilidad, SEO e imágenes está integrada en el hook `scripts/pre-push.sh`. Cada vez que un desarrollador intenta hacer `git push`, el script:

1. Compila y valida `static/css/index.css`.
2. Valida los esquemas YAML de contenido.
3. Ejecuta la suite de tests con cobertura mínima del 85%.
4. **Levanta un servidor temporal de uvicorn** y ejecuta:
   * `scripts/audit_responsive.py` (layout, usabilidad táctil, contraste, foco y accesibilidad con axe-core).
   * `scripts/audit_seo.py` (meta tags, encabezados e imágenes).
5. **Detiene el servidor temporal.**
6. Aborta el push si cualquiera de los pasos anteriores falla.

Si Playwright o **axe-core** no están instalados, el script muestra una advertencia y continúa sin las auditorías correspondientes, pero no bloquea el push.

### Optimización: omisión condicional por tipo de cambio

Para no penalizar pushes que no afectan el frontend, el hook analiza los archivos que se están por pushear y **omite las auditorías responsive y SEO** si **todos** los cambios pertenecen a rutas de exclusión:

* Archivos `.sh`
* `scripts/*` (excepto `scripts/audit_responsive.py`, `scripts/audit_seo.py` y `scripts/audit_components.py`)
* `tests/*`
* `.github/*`
* `.agents/*`
* `docs/*`
* `README.md`, `README`, `AGENTS.md`

Si hay un solo cambio en `templates/`, `static/css/`, `static/js/`, `data/content/`, `src/` o cualquier otro archivo potencialmente relacionado con el frontend, las auditorías se ejecutan normalmente.

### Instalación del hook

```bash
ln -sf ../../scripts/pre-push.sh .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

### Salida esperada

**Con cambios de frontend:**
```text
✅ CSS validado y actualizado.
✅ Todos los esquemas YAML de contenido son válidos.
============================== 51 passed ==============================
✅ Todos los tests pasaron.
==> Verificando auditoría responsive (Playwright)...
...
✅ Auditoría responsive superada. Continuando con el push.
```

**Sin cambios de frontend:**
```text
⏭️ Los cambios a pushear no afectan el frontend. Se omitirá la auditoría responsive.
...
✅ Push validado. Continuando (sin auditoría responsive).
```
