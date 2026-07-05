# Auditoría de Componentes y Responsive (docs/AUDITORIA_COMPONENTES.md)

Este documento detalla la estructura física de los componentes de la interfaz de usuario de **DataMaq**, el estado de su auditoría responsive y usabilidad (Touch Targets) en dispositivos móviles, y las herramientas de telemetría inyectadas en desarrollo.

---

## 1. Mapeo y Estado de la Auditoría

El sistema cuenta con un total de **13 archivos físicos de componentes** en `templates/partials/components/`. Tras la ampliación del enrutador de desarrollo `/dev/preview/*`, **12 componentes son accesibles de forma aislada** para auditoría; el componente `icon.html` es una macro auxiliar de SVG y no requiere previsualización propia.

| Componente | Ruta Física | Previsualización Aislada | Estado | Especificaciones y Correcciones Locales |
| :--- | :--- | :--- | :---: | :--- |
| **Header** | `header.html` | `/dev/preview/header` | **Completado** (✅) | Corregido el bug de especificidad CSS en `.c-home-header__nav` que forzaba el despliegue del menú en móvil, provocando un desborde de `478px` de ancho. En móvil se oculta el menú (`display: none`) y se despliega solo a partir de los `992px`. Touch target de links visibles: **34px** de alto. |
| **Footer** | `footer.html` | `/dev/preview/footer` | **Completado** (✅) | Rediseñado con acordeones nativos en móvil (`<details>` y `<summary>`) con animación y rotación de chevron. El contenido cerrado se oculta mediante `display: none !important`. Restaurada la visibilidad de la marca y datos de contacto en móvil. Altura total móvil reducida de `1140px` a **`700px`**. Touch targets optimizados a **`32px`-`34px`** (cero alertas de usabilidad táctil). |
| **Hero** | `hero.html` | `/dev/preview/hero` | **Completado** (✅) | Sin desbordamientos horizontales ni alertas de Touch Target en viewport de `375px`. La lista de trust-chips utiliza `overflow-x: auto` de forma intencional y controlada; el script de telemetría fue ajustado para ignorar estos contenedores con scroll programado. |
| **Profile** | `profile.html` | `/dev/preview/profile` | **Completado** (✅) | Sin desbordamientos horizontales ni alertas de Touch Target en viewport de `375px`. Avatar, tarjeta de perfil y grilla de beneficios se adaptan correctamente. |
| **Contact Section** | `contact_section.html` + `contact_form.html` | `/dev/preview/contact_section` | **Completado** (✅) | Mejorados los Touch Targets del stepper (`min-height: 2.5rem`) y del enlace de e-mail alternativo (`min-height: 2rem` con `inline-flex`). El stepper se apila en una sola columna en móvil (`max-width: 767.98px`). Botón CTA y campos de formulario mantienen alturas accesibles. |
| **Chatwoot FAB** | `chatwoot_fab.html` | `/dev/preview/chatwoot_fab` | **Completado** (✅) | Botón flotante de `3.5rem × 3.5rem` en móvil (**~56px**), bien por encima del mínimo táctil. No requirió ajustes. |
| **Cookie Banner** | `cookie_banner.html` | `/dev/preview/cookie_banner` | **Completado** (✅) | Botones de acción con `min-height: 2.5rem` en móvil. Se aumentó el área táctil del enlace "Ver más" a `32px` mediante `display: inline-flex`, `align-items: center` y `min-height: 2rem`. |
| **Dock** | `dock.html` | `/dev/preview/dock` | **Completado** (✅) | Barra de navegación fija inferior con enlaces de `min-height: 4.2rem` (variante directa `4.35rem`), equivalente a **~67-70px**. No requirió ajustes. |
| **FAQ Item** | `faq_item.html` | `/dev/preview/faq_item` | **Completado** (✅) | Acordeón nativo con `<summary>` de padding `1.2rem 1.25rem`; el área táctil supera ampliamente los `32px`. No contiene enlaces internos. No requirió ajustes. |
| **Service Card** | `service_card.html` | `/dev/preview/service_card` | **Completado** (✅) | CTA principal con `min-height: 3.2rem` (**~51px**). Contenido, icono y lista de beneficios se adaptan al ancho móvil. No requirió ajustes. |
| **Section Wrapper** | `section_wrapper.html` | `/dev/preview/section_wrapper` | **Completado** (✅) | Envoltura estructurada de secciones. No introduce elementos interactivos propios; su ancho se controla mediante `tw:container tw:mx-auto tw:px-4`. No requirió ajustes. |
| **Icon** | `icon.html` | *No aplica* | **No aplica** (⚪) | Macro de renderizado de iconos SVG de Bootstrap Icons. Es un helper sin interacción propia; se audita indirectamente dentro de los componentes que lo consumen. |

**Resumen:** 12 de 13 componentes auditados, con **0 alertas de Touch Target** en los componentes de bloque principales y **0 desbordamientos horizontales** no intencionales en viewport de `375px`.

---

## 2. Pautas y Estándares de Usabilidad Móvil (UI/UX)

Para garantizar un producto premium, cada componente auditado y refinado en el repositorio debe cumplir rigurosamente con las siguientes pautas ergonómicas antes de ser considerado estable:

* **Sin desbordamiento horizontal:** El scroll horizontal del cuerpo del documento (`document.body.scrollWidth`) debe ser idéntico al ancho del viewport (`window.innerWidth`) en cualquier resolución móvil (típicamente `320px` a `480px`). Los contenedores con `overflow-x: auto` o `overflow-x: scroll` intencionales (p. ej., trust-chips del Hero) se excluyen del reporte.
* **Touch Targets accesibles (WCAG 2.2):**
  * Los elementos de enlace de texto comunes (`<a>`) deben poseer un área táctil física de al menos **`32px` de alto**. Esto se logra incrementando el padding vertical (`padding: .35rem 0`) y usando `display: inline-flex` con `min-height`, sin necesidad de aumentar el tamaño de fuente visual de la tipografía.
  * Los botones de acción principal (`.tw:btn`, `.btn-primary`) deben tener un área de click de al menos **`44px` a `48px` de alto**.
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
   * Análisis automático de Touch Targets indicando la cantidad de enlaces menores a `32px` y listando las alertas con su respectivo tamaño físico.
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

### 4.2. Auditoría responsive y de usabilidad táctil con Playwright

* **Archivo:** [scripts/audit_responsive.py](file:///home/agustin/proyectos_software/www-datamaq/scripts/audit_responsive.py)
* **Dependencias:** [requirements-dev.txt](file:///home/agustin/proyectos_software/www-datamaq/requirements-dev.txt)

**Qué hace:**
1. Abre cada preview en un navegador Chromium headless con viewport móvil.
2. Mide `document.body.scrollWidth` y compara con el ancho del viewport.
3. Detecta elementos con desbordamiento horizontal no intencional (ignora contenedores con `overflow-x: auto/scroll`).
4. Detecta enlaces (`<a>`) con altura inferior a `32px`.
5. Reporta la altura del footer cuando el componente la incluye.

**Instalación:**
```bash
source venv/bin/activate
pip install -r requirements-dev.txt
playwright install chromium
```

**Uso:**
```bash
# Con el servidor de desarrollo corriendo
python3 scripts/audit_responsive.py

# Otro viewport
python3 scripts/audit_responsive.py --viewport 390x844

# Otra URL base
python3 scripts/audit_responsive.py --base-url http://127.0.0.1:5000
```

### Hallazgos y correcciones recientes

Durante la primera corrida de `audit_responsive.py` se detectó que el componente **Dock** con 6 enlaces generaba desbordamiento interno en viewport de `375px` (cada `<a>` medía más de `50px` de ancho real contra los `~50px` disponibles). Se corrigió en `static/css/HomePage.css` estableciendo:

* `grid-template-columns: repeat(var(--dock-columns, 4), minmax(3.5rem, 1fr))` en móvil.
* `overflow-x: auto` y `scroll-snap-type: x mandatory` en el dock para scroll horizontal controlado.
* Texto centrado, ajustable a dos líneas y `font-size` reducido en móvil.

Tras la corrección, la auditoría reporta **0 desbordamientos** y **0 enlaces con touch target insuficiente** en los 13 componentes.
