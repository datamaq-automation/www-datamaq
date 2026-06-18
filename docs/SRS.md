# Especificación de Requisitos del Sistema (SRS) - Datamaq

## Contexto de Migración
Replicar la UI/UX de la versión legacy (Vue.js) bajo arquitectura SSR para optimización SEO.

## 1. Funcionalidades Críticas
- **Landing Page SSR:** SEO optimizado, contenido dinámico desde YAML.
- **Cotizador (Wizard UI):** 
    - **Estrategia:** Multi-paso basado en rutas/parámetros (SSR) para mantener estado y SEO en cada etapa.
    - **UX:** Uso de transiciones CSS para emular la fluidez de Vue.
- **RASA Action Server:** Soporte para lógica de negocio del bot.

## 2. Requisitos No Funcionales
- **Performance:** LCP < 2.5s.
- **Fidelidad:** Coincidencia visual del 100% con el diseño original.
