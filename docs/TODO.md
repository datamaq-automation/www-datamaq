# TODO - Adopción DDD / Arquitectura Limpia

## Tabla de contenidos

1. [Tareas prioritarias](#tareas-prioritarias)
2. [Próximas iteraciones](#próximas-iteraciones)

## Tareas prioritarias

## [Modelado del dominio] Definir `Lead` como Entity y `ContactInfo` como Value Object

- **Severidad:** high
- **Archivo(s):** `src/domain/models.py`
- **Problema:** `ContactSubmitPayload` es un DTO plano; no expresa identidad ni comportamiento de dominio.
- **Oportunidad:** Convertir el payload en `Lead` (Entity con `LeadId`) y `ContactInfo` (Value Object inmutable), manteniendo Pydantic.
- **Acción:** Crear `src/domain/entities/lead.py` y `src/domain/value_objects/contact_info.py`.
- **Bloqueado por:** Ninguna.
- **Estimación:** S

## [Repository pattern] Extraer persistencia JSON a interfaz + implementación

- **Severidad:** high
- **Archivo(s):** `src/infrastructure/fastapi/routes/contact_routes.py`
- **Problema:** `persist_lead_task` abre archivos directamente dentro del router.
- **Oportunidad:** Repository pattern: el dominio define el puerto, la infraestructura provee la implementación JSON.
- **Acción:** Crear `src/domain/repositories/lead_repository.py` y `src/infrastructure/persistence/json/lead_repository_json.py`.
- **Bloqueado por:** Tarea 2.
- **Estimación:** S

## [Gateway externo] Crear adaptador para Chatwoot Application API

- **Severidad:** medium
- **Archivo(s):** Nuevo adaptador
- **Problema:** No existe integración con Chatwoot Application API; solo hay SDK de widget en frontend.
- **Oportunidad:** Gateway pattern: aísla el cliente HTTP de Chatwoot del resto de la aplicación.
- **Acción:** Crear `src/application/gateways/chatwoot_gateway.py` (interfaz) y `src/infrastructure/gateways/chatwoot_gateway_http.py`.
- **Bloqueado por:** Ninguna.
- **Estimación:** M

## [Caso de Uso] Implementar `SubmitLeadUseCase`

- **Severidad:** high
- **Archivo(s):** Nuevo use case
- **Problema:** No hay un único punto que orqueste guardar lead + crear contacto/conversación.
- **Oportunidad:** Application Service que coordina Repository + Gateway sin reglas de negocio complejas.
- **Acción:** Crear `src/application/use_cases/submit_lead.py` con `execute(payload) -> LeadSubmissionResult`.
- **Bloqueado por:** Tareas 2, 3 y 4.
- **Estimación:** M

## [Inyección de dependencias] Proveer repository y gateway desde `dependencies.py`

- **Severidad:** medium
- **Archivo(s):** `src/infrastructure/fastapi/dependencies.py`
- **Problema:** Solo provee `DataService`; no inyecta repositorios ni gateways.
- **Oportunidad:** Extender el contenedor ligero de FastAPI para inyectar implementaciones de infraestructura.
- **Acción:** Agregar `get_lead_repository()` y `get_chatwoot_gateway()`; usarlos en `contact_routes.py`.
- **Bloqueado por:** Tareas 3 y 4.
- **Estimación:** XS

## [Mapeo entre capas] Definir traducción Pydantic payload → Entity → DTO Chatwoot

- **Severidad:** medium
- **Archivo(s):** `src/domain/models.py`, nuevos mappers
- **Problema:** No hay mapper explícito; el controller usaría directamente el payload Pydantic.
- **Oportunidad:** Mapper/Translator para mantener al dominio libre de formatos externos.
- **Acción:** Crear `src/application/mappers/lead_mapper.py` y `chatwoot_conversation_mapper.py`.
- **Bloqueado por:** Tarea 2.
- **Estimación:** S

## [Manejo de errores entre capas] Definir política de fallo parcial

- **Severidad:** critical
- **Archivo(s):** `src/application/use_cases/submit_lead.py`, gateway Chatwoot
- **Problema:** Si Chatwoot falla después de guardar el lead, perdemos trazabilidad o confundimos al usuario.
- **Oportunidad:** Domain Event o registro de estado de sincronización; nunca perder el lead por fallo externo.
- **Acción:** Crear `LeadSubmissionResult` con `lead_saved` y `chatwoot_synced`; si Chatwoot falla, devolver éxito parcial y loggear reintento.
- **Bloqueado por:** Tarea 5.
- **Estimación:** M

## Próximas iteraciones

1. **Eventos de dominio (`LeadSubmitted`):** publicar un evento al guardar un lead y que Chatwoot se suscriba.
2. **Validaciones de dominio en `Lead`:** mover reglas como "email o teléfono requerido" desde Pydantic hacia la entidad.
3. **Caché de contenido estático:** aplicar un Repository en `DataService` para evitar leer YAML en cada request.


# Tareas pendientes — Datamaq

> Estado actual: Etapa 1 (Estabilización del deploy) completada. El deploy automático funciona con el workflow `.github/workflows/deploy.yml`, usuario `datamaq` no privilegiado, SSH por clave y Python 3.12. El CI corre localmente mediante `scripts/pre-push.sh`. La Etapa 2 (GitHub Actions) está completada: secrets configurados y rollback implementado.

## DevOps / CI-CD — Migración a GitHub Actions

### P0 — Crítico

_Completado: ver `docs/TODO.done.md`._

### P1 — Necesario

_Completado: ver `docs/TODO.done.md`._

### P2 — Deseable

_Completado: ver `docs/TODO.done.md`._

---

## SEO — Iteración actual

> Basado en el informe de auditoría SEO técnica. Cada ítem referencia el hallazgo correspondiente del informe.

### P1 — Crítico

- [ ] **P1-SEO-02** Diferenciar contenido de páginas dinámicas (localidad e industria) para mitigar thin content y contenido duplicado.
  - *Referencia:* Informe SEO, oportunidad #2.
  - *Nota:* Home, localidades e industrias comparten el mismo template `index.html` con ~90 % de contenido idéntico.

- [x] **P1-SEO-03** Implementar normalización de URLs en la aplicación (HTTP→HTTPS, trailing slash, www/no-www) o validar que el reverse proxy ya la realice.
  - *Referencia:* Informe SEO, oportunidad #3.
  - *Nota:* Middleware `canonical_redirect_middleware` agregado en `src/infrastructure/fastapi/middleware.py`. Normaliza www→no-www, trailing slash y HTTP→HTTPS cuando el reverse proxy envía `X-Forwarded-Proto: http`.

### P2 — Mejora

- [ ] **P2-SEO-05** Reemplazar el favicon SVG usado como `logo` en Schema.org por una imagen cuadrada representativa de marca.
  - *Referencia:* Informe SEO, oportunidad #5.

- [ ] **P2-SEO-06** Permitir configurar `og:image` específico por localidad e industria en los archivos YAML.
  - *Referencia:* Informe SEO, oportunidad #6.

- [ ] **P2-SEO-07** Agregar `hreflang="x-default"` junto al `hreflang="es_AR"` existente.
  - *Referencia:* Informe SEO, oportunidad #8.

### P3 — Optimización futura

- [ ] **P3-SEO-09** Eliminar preconnects a Google Fonts si no se cargan fuentes, o agregar la hoja de estilos correspondiente.
  - *Referencia:* Informe SEO, oportunidad #9.

- [ ] **P3-SEO-10** Proveer favicon en formatos PNG/ICO además del SVG actual.
  - *Referencia:* Informe SEO, oportunidad #10.

- [ ] **P3-SEO-11** Definir si se activa o elimina el script comentado de Cloudflare beacon.
  - *Referencia:* Informe SEO, oportunidad #11.

---

## Pendientes de decisión

> Items cuya certeza en el informe es "Duda" o "Requiere validación". Requieren una decisión estratégica antes de convertirse en tareas de implementación.

- [ ] **DEC-SEO-01** Definir si `/terminos-y-condiciones` debe permanecer indexable (`index,follow`) o pasar a `noindex,follow`.
  - *Referencia:* Informe SEO, oportunidad #7.
  - *Certeza:* Requiere validación.
  - *Pendiente:* Decisión de estrategia de contenido legal.

- [ ] **DEC-SEO-02** Confirmar si el reverse proxy de producción (Nginx/Cloudflare) ya realiza redirecciones HTTP→HTTPS y normalización de trailing slash/www.
  - *Referencia:* Informe SEO, oportunidad #3.
  - *Certeza:* Requiere validación.
  - *Pendiente:* Validación de infraestructura antes de implementar middleware de respaldo en FastAPI.

---

## Bloqueos

> Actualizado: la Etapa 2 (GitHub Actions) está completada. No hay bloqueos activos.

_No hay bloqueos activos._