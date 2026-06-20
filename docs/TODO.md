# Tareas pendientes — Datamaq

> Estado actual: Etapa 1 (Estabilización del deploy) completada. El deploy manual funciona con usuario `datamaq` no privilegiado, SSH por clave y Python 3.12. La Etapa 2 (GitHub Actions) está lista para iniciar.

## DevOps / CI-CD — Migración a GitHub Actions

### P0 — Crítico

- [ ] **P0-GHA-01** Crear workflow de CI (test) en `.github/workflows/ci.yml`.
  - **Archivos afectados:** `.github/workflows/ci.yml`
  - **Riesgo si no se hace:** No hay validación automática antes del deploy.
  - **Criterio de aceptación mínimo:** Cada push/PR a `main` ejecuta `pytest` con cobertura mínima del `85 %`.

### P1 — Necesario

- [ ] **P1-GHA-03** Migrar secrets de `scripts/.env.deploy` a GitHub Secrets.
  - **Archivos afectados:** Configuración del repositorio en GitHub
  - **Riesgo si no se hace:** Las credenciales permanecen en el disco local del desarrollador.
  - **Criterio de aceptación mínimo:** Los workflows leen `DEPLOY_SSH_HOST`, `DEPLOY_SSH_PORT`, `DEPLOY_SSH_USER` y `DEPLOY_SSH_KEY` desde GitHub Secrets.

### P2 — Deseable

- [ ] **P2-GHA-04** Implementar rollback automático en el workflow de deploy.
  - **Archivos afectados:** `.github/workflows/deploy.yml`, `scripts/deploy-server.sh`
  - **Riesgo si no se hace:** Un deploy fallido requiere intervención manual.
  - **Criterio de aceptación mínimo:** Si el health-check falla, el workflow ejecuta rollback y notifica el fallo.

---

## SEO — Iteración actual

> Basado en el informe de auditoría SEO técnica. Cada ítem referencia el hallazgo correspondiente del informe.

### P1 — Crítico

- [ ] **P1-SEO-02** Diferenciar contenido de páginas dinámicas (localidad e industria) para mitigar thin content y contenido duplicado.
  - *Referencia:* Informe SEO, oportunidad #2.
  - *Nota:* Home, localidades e industrias comparten el mismo template `index.html` con ~90 % de contenido idéntico.

- [ ] **P1-SEO-03** Implementar normalización de URLs en la aplicación (HTTP→HTTPS, trailing slash, www/no-www) o validar que el reverse proxy ya la realice.
  - *Referencia:* Informe SEO, oportunidad #3.
  - *Nota:* Actualmente no hay middleware en FastAPI que redirija a la versión canónica.

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

> Actualizado: el deploy manual es funcional y el workflow de CD en GitHub Actions está implementado. Queda pendiente configurar los secrets en GitHub.

1. **P1-GHA-03** debe completarse antes de que el workflow de deploy funcione: los secrets de GitHub (`DEPLOY_SSH_HOST`, `DEPLOY_SSH_PORT`, `DEPLOY_SSH_USER`, `DEPLOY_SSH_KEY`) deben estar configurados.
2. **P2-GHA-04** depende de **P0-DEV-03**: el rollback automático en GitHub Actions requiere que `scripts/deploy-server.sh` ya tenga rollback implementado.

---

## Notas de implementación

- El entorno de producción ahora usa Python 3.12 compilado en `/usr/local/bin/python3.12`.
- El entorno virtual de producción está en `/var/www/www-datamaq/.venv`.
- El servicio systemd es `datamaq.service`.
- La clave SSH para deploy está en `~/.ssh/datamaq_deploy` (local) y `/home/datamaq/.ssh/authorized_keys` (VPS).
