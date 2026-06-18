# Plan de Migración (TODO)

## Fase 1: Estructura de Componentes
- [ ] Crear directorio `templates/partials/macros/`.
- [ ] Migrar Header y Footer (Fidelidad 100%).
- [ ] Implementar Macro de Servicios basada en `industrias.yaml`.

## Fase 2: Lógica de Negocio y Wizard
- [ ] Definir rutas de FastAPI para los pasos del Cotizador.
- [ ] Implementar lógica de persistencia de estado del Wizard (Session/Cookies).
- [ ] Replicar UI del Cotizador de Vue.

## Fase 3: Bot e Integración
- [ ] Implementar endpoint de RASA Action Server.
- [ ] Validar integración Chatwoot + RASA.
