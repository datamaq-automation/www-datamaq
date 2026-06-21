# Reporte DDD - Diagnóstico de Arquitectura

**Fecha:** 2026-06-20
**Scope:** Módulo de captura de leads + integración Chatwoot

## Tabla de contenidos

1. [Estado actual (AS-IS)](#1-estado-actual-as-is)
2. [Modelo de dominio propuesto (TO-BE)](#2-modelo-de-dominio-propuesto-to-be)
3. [Bounded Contexts identificados](#3-bounded-contexts-identificados)
4. [Mapa de dependencias actuales](#4-mapa-de-dependencias-actuales)
5. [Riesgos y mitigaciones](#5-riesgos-y-mitigaciones)
6. [Glosario de términos DDD](#6-glosario-de-términos-ddd)

## 1. Estado actual (AS-IS)

El flujo de captura de leads funciona así:

1. **Frontend:** `FormManager.js` recolecta datos y envía POST a `/api/v1/contact`.
2. **Controller:** `contact_routes.py` recibe `ContactSubmitPayload`, genera IDs con `uuid`, llama a `persist_lead_task` como `BackgroundTasks` y escribe JSON en `data/leads/`.
3. **Chatwoot hoy:** solo existe integración de widget vía SDK en `ChatwootManager.js`. No hay creación de Contact desde backend.
4. **Contenido estático:** `DataService` lee YAML y lo valida con Pydantic.

**Lo que está bien:** separación física de carpetas (`domain/`, `application/`, `infrastructure/`) y uso de Pydantic para validar payloads.

**Lo que está mezclado:** `contact_routes.py` acumula controller, generación de IDs, persistencia y orquestación.

## 2. Modelo de dominio propuesto (TO-BE)

```text
Lead (Entity)
├── LeadId (Value Object)
├── ContactInfo (Value Object)
├── comment, preferred_channel, page_location, submitted_at, tenant_id

SubmitLeadUseCase (Application Service)
├── LeadRepository (port)
├── ChatwootGateway (port)
└── LeadMapper / ChatwootContactMapper

LeadRepositoryJson (Infrastructure)
ChatwootGatewayHttp (Infrastructure)
```

- **Entity:** `Lead` (tiene identidad y ciclo de vida).
- **Value Objects:** `LeadId`, `ContactInfo` (inmutables).
- **Application Service:** `SubmitLeadUseCase` orquesta guardar lead y crear contacto en Chatwoot.
- **Repository:** `LeadRepository` abstrae dónde se guarda el lead.
- **Gateway:** `ChatwootGateway` abstrae la API externa.

## 3. Bounded Contexts identificados

| Contexto | Responsabilidad | Por qué es separado |
|---|---|---|
| **Landing Page / Captura de Leads** | Renderizar páginas, recibir formulario. | Lenguaje: lead, formulario, consulta. |
| **Integración Chatwoot** | Crear contacts vía Application API. | Sistema externo; lenguaje: contacto, inbox. |
| **Contenido Estático** | YAML, SEO, CTAs, datos geográficos. | Read-only para la landing; sin reglas de negocio de leads. |

## 4. Mapa de dependencias actuales

```text
FormManager.js → POST /api/v1/contact
contact_routes.py → ContactSubmitPayload, persist_lead_task, BackgroundTasks, templates
data_service.py → ContenidoModel, yaml
dependencies.py → DataService, config, logger
```

**Dependencias que violan Arquitectura Limpia:**

- ⚠️ `contact_routes.py` contiene lógica de persistencia (`persist_lead_task`). La capa de infraestructura no debería saber cómo escribir JSON.
- ⚠️ `contact_routes.py` genera IDs y orquesta. Eso pertenece a la capa de aplicación.

**Lo que respeta la regla:** `DataService` depende de modelos de dominio, no al revés.

## 5. Riesgos y mitigaciones

| Riesgo | Descripción | Mitigación |
|---|---|---|
| **Técnico: romper el formulario** | Extraer use case puede cambiar respuesta HTTP o JSON guardado. | Mantener contrato de `/api/v1/contact` idéntico; cambiar solo implementación interna. |
| **Técnico: Chatwoot no responde** | El usuario recibe error aunque el lead esté guardado. | Guardar lead primero; Chatwoot best-effort con reintento asíncrono. |
| **De negocio: lead sin contacto en Chatwoot** | Perdemos visibilidad del lead si Chatwoot falla. | Registrar `chatwoot_synced` y alertar si falla. |
| **Complejidad: sobre-ingeniar** | DDD puede generar muchas clases para un flujo simple. | Aplicar solo patrones necesarios; mantener Pydantic. |

## 6. Glosario de términos DDD

| Término | Definición en nuestro dominio |
|---|---|
| **Lead** | Solicitud de contacto desde el formulario. Tiene identidad (`LeadId`) y ciclo de vida. |
| **ContactInfo** | Datos de contacto del lead. Inmutable y sin identidad propia. |
| **Conversation** | Hilo de mensajes en Chatwoot. No se crea automáticamente desde el formulario. |
| **Gateway** | Adaptador que aísla las llamadas HTTP a la API de Chatwoot. |
| **Repository** | Abstracción para guardar/recuperar leads sin que el dominio sepa el storage. |
| **Use Case** | Orquestación de un flujo de negocio, ej. guardar lead + crear contacto en Chatwoot. |
| **Controller** | Router de FastAPI que recibe request, delega al use case y responde HTTP. |
| **Aggregate** | Grupo tratado como unidad; `Lead` es el aggregate root de leads. |
| **Domain Event** | Notificación de que algo importante ocurrió, ej. `LeadSubmitted`. |
