# Informe de cambios — 6 de agosto de 2026

> **Destinatario:** Claude Code en el VPS (168.181.184.103)
> **Propósito:** Documentar los cambios realizados para que otra instancia de Claude en el VPS entienda el nuevo stack y pueda operar/solucionar problemas.

---

## 1. Resumen ejecutivo

Se realizaron dos cambios mayores en `www-datamaq`:

1. **Reposicionamiento estratégico:** de "consultor IoT Zona Norte GBA" a "contratista de mantenimiento eléctrico Oil & Gas — Vaca Muerta"
2. **Eliminación de Chatwoot:** reemplazado por WhatsApp FAB + notificaciones por email vía SMTP (Exim del VPS)

Ambos cambios están deployados en producción (`datamaq.com.ar`) a través del commit `2fc06a5`.

---

## 2. Nuevo stack de notificaciones (reemplaza Chatwoot)

### 2.1. Arquitectura

```
Usuario llena formulario en datamaq.com.ar
  → POST /api/v1/contact
    → SubmitLeadUseCase
      ├── LeadRepositoryJson → data/leads/{submission_id}.json  (fuente de verdad)
      └── EmailNotificationGateway → SMTP localhost:587 (Exim) → email a agustin@datamaq.com.ar
```

### 2.2. Gateway (patrón hexagonal)

El puerto es `NotificationGateway` (ABC, método `notify_lead(lead_data) -> Dict`). Dos implementaciones:

| Implementación | Archivo | Cuándo se usa |
|---|---|---|
| `EmailNotificationGateway` | `src/infrastructure/gateways/email_notification_gateway.py` | Si `SMTP_USERNAME`, `SMTP_PASSWORD` y `NOTIFICATION_EMAIL` están configurados |
| `NotificationGatewayStub` | `src/infrastructure/gateways/notification_gateway_stub.py` | Si faltan credenciales SMTP — solo loguea, no envía |

La selección ocurre en `src/infrastructure/fastapi/dependencies.py` → `get_notification_gateway()`.

### 2.3. Variables de entorno (`.env` en el VPS)

```env
SMTP_HOST=localhost
SMTP_PORT=587
SMTP_USERNAME=no-reply@datamaq.com.ar
SMTP_PASSWORD=****
NOTIFICATION_EMAIL=agustin@datamaq.com.ar
WHATSAPP_PHONE=541156297160
```

`SMTP_HOST=localhost` porque Exim corre en el mismo VPS. Si la app se corre desde otro lado (dev local), debe apuntar a `168.181.184.103`.

### 2.4. WhatsApp FAB

El botón flotante de Chatwoot fue reemplazado por un botón de WhatsApp. Es un `<a href="wa.me/...">` nativo, sin SDK, sin JavaScript.

- Template: `templates/partials/components/whatsapp_fab.html`
- CSS: `static/css/WhatsappFab.css` (verde `#25d366`, importado desde `input.css`)
- Config: `config.WHATSAPP_PHONE` y `config.WHATSAPP_MESSAGE`

---

## 3. Reposicionamiento Oil & Gas

### 3.1. Archivos de contenido modificados

Todo el contenido es data-driven (YAML). Los cambios están en:

| Archivo | Qué cambió |
|---------|-----------|
| `data/seo/seo.yaml` | Title, description → enfocados en mantenimiento eléctrico O&G |
| `data/content/home_sections.yaml` | Hero, servicios (MT/BT, VFD, Electrógenos, Eficiencia), FAQ, About, perfil |
| `data/config/brand.yaml` | Rol del técnico, bio, footer description |
| `data/meta/geografia.yaml` | Agregada provincia de Neuquén (Confluencia + Añelo, 6 localidades) |
| `data/meta/industrias.yaml` | Agregadas industrias "Oil & Gas" y "Energía" |
| `data/seo/landing_content.yaml` | Contenido SEO para Neuquén (6 localidades) + Oil & Gas + Energía |
| `data/core/casos/{3 nuevos}/caso.yaml` | Casos: diagnóstico VFD compresora, adecuación CCM, medición aislación MT |

### 3.2. Cero cambios en código

No se tocó `src/`, `templates/`, ni `static/` para el reposicionamiento. Solo YAML.

---

## 4. Archivos eliminados

```
src/application/gateways/chatwoot_gateway.py
src/application/dtos/chatwoot_contact_dto.py
src/application/mappers/chatwoot_contact_mapper.py
src/infrastructure/gateways/chatwoot_gateway_http.py
src/infrastructure/gateways/chatwoot_gateway_stub.py
static/js/modules/ChatwootManager.js
templates/partials/components/chatwoot_fab.html
static/css/ChatwootFab.css
scripts/test_chatwoot.sh
```

---

## 5. Archivos nuevos

```
src/application/gateways/notification_gateway.py         (ABC)
src/infrastructure/gateways/email_notification_gateway.py (SMTP)
src/infrastructure/gateways/notification_gateway_stub.py  (dev fallback)
templates/partials/components/whatsapp_fab.html           (botón WhatsApp)
static/css/WhatsappFab.css                                (estilos verde WhatsApp)
data/core/casos/diagnostico-vfd-compresion/caso.yaml
data/core/casos/adecuacion-tablero-ccm/caso.yaml
data/core/casos/medicion-aislacion-mt/caso.yaml
```

---

## 6. Troubleshooting

### El formulario devuelve `submitStatus: "partial_success"`

El lead se guardó en `data/leads/` pero el email no se envió. Verificar:

```bash
# Logs de la app
journalctl -u datamaq.service --since "5 minutes ago" --no-pager

# Exim corriendo?
ss -tlnp | grep 587
```

Causas probables:
- Exim no está corriendo → `systemctl restart exim`
- Credenciales SMTP incorrectas → verificar `.env`
- La app no puede conectar a `localhost:587`

### El lead se guarda pero no se notifica (stub activo)

Si los logs dicen `[NotificationGatewayStub]` en vez de `[EmailNotificationGateway]`, las variables SMTP no están configuradas. Verificar `.env` en `/var/www/www-datamaq/.env`.

### Reconstruir CSS

Si se edita `static/css/WhatsappFab.css` o `static/css/src/input.css`:

```bash
cd /var/www/www-datamaq
source venv/bin/activate
npm run build:css
systemctl restart datamaq.service
```

### Testear envío de email manualmente

```bash
curl -X POST https://datamaq.com.ar/api/v1/contact \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","comment":"Prueba","email":"agustin@datamaq.com.ar","createdAt":"2026-08-06T00:00:00Z","pageLocation":"https://datamaq.com.ar/contact"}'
```

### Pipeline de pre-push

El hook `.git/hooks/pre-push` ejecuta:
1. `npm run build:css` — verifica CSS actualizado
2. `python scripts/validate_content.py` — valida YAML
3. `pytest` — 67 tests
4. `python scripts/audit_responsive.py` — Playwright en 13 componentes × 3 viewports
5. `python scripts/audit_seo.py` — Playwright en 5 rutas

Cualquier falla bloquea el push. Los tests toman ~85s en total. Si falla por un overflow de 3px en mobile, es intencional — corregir el CSS fuente y rebuild-ear.

---

## 7. Health check rápido

```bash
# Sitio vivo
curl -sI https://datamaq.com.ar/ | head -1  # 200 OK

# API de contacto
curl -s -X POST https://datamaq.com.ar/api/v1/contact \
  -H "Content-Type: application/json" \
  -d '{"name":"Health Check","comment":"test","createdAt":"2026-01-01T00:00:00Z","pageLocation":"https://datamaq.com.ar/"}' \
  | jq .submitStatus  # "success" o "partial_success"

# WhatsApp FAB presente
curl -s https://datamaq.com.ar/ | grep -q "c-whatsapp-fab" && echo "OK" || echo "FALTA"

# Sin rastros de Chatwoot
curl -s https://datamaq.com.ar/ | grep -ci "chatwoot"  # debe ser 0
```

---

## 8. Commits incluidos en este deploy

```
2fc06a5 fix(css): Add overflow-wrap to hero title to prevent mobile overflow
d920a15 fix(css): Rename ChatwootFab to WhatsappFab, update styles to WhatsApp green
aa5b960 refactor: Remove Chatwoot integration script
7fc585c Refactor: Remove Chatwoot integration and replace with WhatsApp contact button
ea7eb85 feat: Add case studies for Oil & Gas sector and update geo/industry metadata
```
