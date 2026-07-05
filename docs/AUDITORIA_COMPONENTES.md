# Auditoría de Componentes y Responsive (docs/AUDITORIA_COMPONENTES.md)

Este documento detalla la estructura física de los componentes de la interfaz de usuario de **DataMaq**, el estado de su auditoría responsive y usabilidad (Touch Targets) en dispositivos móviles, y las herramientas de telemetría inyectadas en desarrollo.

---

## 1. Mapeo y Estado de la Auditoría

El sistema cuenta con un total de **13 archivos físicos de componentes**, de los cuales **5 componentes de bloque principales** están mapeados y son accesibles de forma aislada a través del enrutador de desarrollo `/dev/preview/*`.

| Componente | Ruta Física | Previsualización Aislada | Estado | Especificaciones y Correcciones Locales |
| :--- | :--- | :--- | :---: | :--- |
| **Header** | `header.html` | `/dev/preview/header` | **Completado** (✅) | Corregido el bug de especificidad CSS en `.c-home-header__nav` que forzaba el despliegue del menú en móvil, provocando un desborde de `478px` de ancho. En móvil se oculta el menú (`display: none`) y se despliega solo a partir de los `992px`. Touch target de links visibles: **34px** de alto. |
| **Footer** | `footer.html` | `/dev/preview/footer` | **Completado** (✅) | Rediseñado a doble columna en mobile (apilado vertical asimétrico `1fr 1.5fr` en tablets y `1fr 2fr 1fr` en desktop). Implementados acordeones nativos en móvil (`<details>` y `<summary>`) con animación y rotación de chevron. El contenido cerrado se oculta mediante `display: none !important`. Restaurada la visibilidad de la marca y datos de contacto en móvil. Altura total móvil reducida de `1140px` a **`700px`**. Touch targets optimizados a **`32px`-`34px`** (cero alertas de usabilidad táctil). |
| **Hero** | `hero.html` | `/dev/preview/hero` | *Pendiente* (⏳) | Por auditar. Requiere revisar el desborde horizontal de los trust-chips en pantallas móviles reportado en la telemetría global (`ancho_real_px: 676px`). |
| **Profile** | `profile.html` | `/dev/preview/profile` | *Pendiente* (⏳) | Por auditar. Perfil técnico de instructores y staff de capacitación. |
| **Contact Section** | `contact_section.html` y `contact_form.html` | `/dev/preview/contact_section` | *Pendiente* (⏳) | Por auditar. Formulario dinámico de contacto en pasos de conversión de leads. |
| **Chatwoot FAB** | `chatwoot_fab.html` | *No soportado* | *Pendiente* (⏳) | Botón flotante de mensajería interactiva (Chatwoot). |
| **Cookie Banner** | `cookie_banner.html` | *No soportado* | *Pendiente* (⏳) | Banner flotante de consentimiento de cookies de terceros. |
| **Dock** | `dock.html` | *No soportado* | *Pendiente* (⏳) | Barra de navegación fija inferior móvil (`display: grid` a 4 columnas). Mide `576px` de ancho en móviles, requiere revisión de encogimiento. |
| **FAQ Item** | `faq_item.html` | *No soportado* | *Pendiente* (⏳) | Acordeón nativo de preguntas frecuentes. |
| **Service Card** | `service_card.html` | *No soportado* | *Pendiente* (⏳) | Tarjetas de propuesta de soluciones técnicas industriales. |
| **Section Wrapper** | `section_wrapper.html` | *No soportado* | *Pendiente* (⏳) | Envoltura estructurada de secciones. |
| **Icon** | `icon.html` | *No soportado* | *No aplica* | Macro de renderizado de iconos SVG de Bootstrap Icons. |

---

## 2. Pautas y Estándares de Usabilidad Móvil (UI/UX)

Para garantizar un producto premium, cada componente auditado y refinado en el repositorio debe cumplir rigurosamente con las siguientes pautas ergonómicas antes de ser considerado estable:

* **Sin desbordamiento horizontal:** El scroll horizontal del cuerpo del documento (`document.body.scrollWidth`) debe ser idéntico al ancho del viewport (`window.innerWidth`) en cualquier resolución móvil (típicamente `320px` a `480px`).
* **Touch Targets accesibles (WCAG 2.2):**
  * Los elementos de enlace de texto comunes (`<a>`) deben poseer un área táctil física de al menos **`32px` de alto**. Esto se logra incrementando el padding vertical (`padding: .35rem 0`) y line-height, sin necesidad de aumentar el tamaño de fuente visual de la tipografía.
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
