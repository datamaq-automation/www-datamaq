# Instrucciones y Reglas de Desarrollo para Agentes de IA (AGENTS.md)

Este archivo contiene los lineamientos de diseño, restricciones arquitectónicas y reglas de comportamiento que todo asistente de desarrollo de Inteligencia Artificial (como Antigravity, Kimi Code o Codex) debe obedecer al trabajar en el repositorio **www-datamaq**.

---

## 1. Idioma de Interacción y Documentación
* **Idioma:** Toda comunicación con el usuario en el chat, logs de descubrimiento, explicaciones de commits y documentación técnica nueva (`*.md`) debe redactarse **exclusivamente en español**.

---

## 2. Restricciones de Arquitectura y Diseño de Software
* **Arquitectura Hexagonal / Limpia:** La aplicación en [src/](file:///home/agustin/proyectos_software/www-datamaq/src) está organizada en capas con responsabilidades delimitadas que deben mantenerse:
  * **[domain/](file:///home/agustin/proyectos_software/www-datamaq/src/domain)**: Define las entidades y modelos de datos estrictamente usando Pydantic. No debe depender de ninguna librería de infraestructura (como FastAPI o bases de datos).
  * **[application/](file:///home/agustin/proyectos_software/www-datamaq/src/application)**: Contiene los servicios de aplicación y casos de uso (ej. `DataService`).
  * **[infrastructure/](file:///home/agustin/proyectos_software/www-datamaq/src/infrastructure)**: Inicialización de FastAPI, configuración de rutas web y middleware.
* **Separación de Lógica:** No se permite escribir lógica de acceso a datos o de negocio directamente dentro de los endpoints de rutas en [infrastructure/fastapi/routes/](file:///home/agustin/proyectos_software/www-datamaq/src/infrastructure/fastapi/routes). Estos deben limitarse a recibir peticiones, llamar al servicio correspondiente y retornar la plantilla o respuesta.

---

## 3. Gestión de Datos de Contenido (Servicios, Cobertura, Leads y Cursos)
* **Datos Desacoplados:** Toda la información referente a la propuesta de servicios técnicos, industrias asociadas, cobertura geográfica, leads capturados, cursos, lecciones, cuestionarios e instructores reside en archivos estáticos en la carpeta [data/](file:///home/agustin/proyectos_software/www-datamaq/data).
* **Prohibido Hardcodear:** No debes escribir datos de contenido o textos descriptivos dentro del código Python o directamente en las plantillas HTML de [templates/](file:///home/agustin/proyectos_software/www-datamaq/templates). Toda incorporación de información debe realizarse actualizando los archivos `.yaml` y agregando los archivos `.md` correspondientes.

---

## 4. Control de Calidad y Pruebas
* **Pruebas Automatizadas Obligatorias:** Tras realizar cualquier modificación al código fuente, debes ejecutar las pruebas unitarias y de integración para garantizar que no existan regresiones:
  ```bash
  pytest
  ```
* **Verificación de Cobertura:** Asegúrate de no reducir la cobertura de pruebas al añadir nueva lógica o rutas. Puedes verificar la cobertura ejecutando:
  ```bash
  pytest --cov=src tests/
  ```

---

## 5. Control de Cambios y Despliegue
* **Despliegues con Autorización:** Está prohibido ejecutar el despliegue automático hacia producción (`deploy-server.sh`) de manera autónoma. Cualquier despliegue debe ser explícitamente aprobado por el usuario.
* **Validación de Dependencias:** Al añadir librerías nuevas al archivo [requirements.txt](file:///home/agustin/proyectos_software/www-datamaq/requirements.txt) , valida primero localmente que no existan conflictos de versiones.
