# Tareas pendientes — Datamaq

> Estado actual: Etapa 1 (Estabilización del deploy) completada. El deploy manual funciona con usuario `datamaq` no privilegiado, SSH por clave y Python 3.12. La Etapa 2 (GitHub Actions) está lista para iniciar.

## DevOps / CI-CD — Estabilización del deploy actual

### P0 — Crítico

- [x] **P0-DEV-01** Eliminar/rotar credenciales hardcodeadas en `scripts/.env.deploy` y prohibir deploy como `root`.
  - **Archivos afectados:** `scripts/.env.deploy`, `scripts/deploy-server.sh`, `scripts/view_logs.sh`
  - **Riesgo si no se hace:** Exposición total del VPS, ejecución de la app con privilegios de root e incumplimiento de `AGENTS.md`.
  - **Criterio de aceptación mínimo:** `scripts/.env.deploy` no contiene usuario `root` ni IP/puerto SSH en texto plano; el deploy se ejecuta con un usuario dedicado no privilegiado.

- [x] **P0-DEV-02** Crear usuario dedicado en el VPS para deploy y ejecución de la app.
  - **Archivos afectados:** Configuración del VPS (fuera del repo), `/etc/systemd/system/datamaq.service`, `scripts/deploy-server.sh`, `scripts/setup-vps-user.sh`
  - **Riesgo si no se hace:** Bloquea toda la migración a CI/CD seguro; el servicio sigue corriendo como `root` o con permisos mixtos.
  - **Criterio de aceptación mínimo:** Existe un usuario `datamaq` con shell `bash`, propietario de `/var/www/www-datamaq`, y el servicio corre con ese usuario.

- [ ] **P0-DEV-03** Implementar rollback en `scripts/deploy-server.sh`.
  - **Archivos afectados:** `scripts/deploy-server.sh`
  - **Riesgo si no se hace:** Un deploy fallado deja el sitio caído sin mecanismo de recuperación automática.
  - **Criterio de aceptación mínimo:** El script guarda `HEAD` antes del `git pull`, ejecuta health-check HTTP, y en caso de fallo ejecuta `git reset --hard <commit-previo>` y reinicia el servicio.

### P1 — Necesario

- [ ] **P1-DEV-04** Añadir health-check real al deploy.
  - **Archivos afectados:** `scripts/deploy-server.sh`, posiblemente `src/infrastructure/fastapi/routes/main_routes.py`
  - **Riesgo si no se hace:** `systemctl is-active` solo verifica el proceso, no que la app responda correctamente.
  - **Criterio de aceptación mínimo:** Después del restart, el script hace una petición HTTP a `http://localhost:8000/` y valida status `200`.

- [x] **P1-DEV-05** Sincronizar `docs/CD.md` con la realidad del repositorio.
  - **Archivos afectados:** `docs/CD.md`
  - **Riesgo si no se hace:** La documentación miente sobre el estado del CI/CD y causa errores al seguirla.
  - **Criterio de aceptación mínimo:** `docs/CD.md` no menciona `backend/requirements.txt` ni asume que existe un workflow de GitHub Actions.

- [x] **P1-DEV-06** Sincronizar `scripts/.env.deploy.example` con el flujo real.
  - **Archivos afectados:** `scripts/.env.deploy.example`
  - **Riesgo si no se hace:** Un nuevo desarrollador no sabe qué variables son obligatorias ni cuáles son los valores esperados.
  - **Criterio de aceptación mínimo:** El template documenta cada variable, su ejemplo seguro, el nombre del servicio (`datamaq.service`) y una advertencia explícita de no usar `root`.

### P2 — Deseable

- [x] **P2-DEV-07** Estandarizar nombres: `datamaq` en lugar de `electricista380`.
  - **Archivos afectados:** `docs/CD.md`, `AGENTS.md`, `scripts/deploy-server.sh`, `scripts/view_logs.sh`, `scripts/setup-vps-user.sh`, servicio systemd
  - **Riesgo si no se hace:** Deuda técnica y confusión operativa entre el nombre del proyecto, del dominio y del servicio.
  - **Criterio de aceptación mínimo:** Decisión documentada y nombres consistentes en todo el repositorio y el VPS.

---

## DevOps / CI-CD — Migración a GitHub Actions

### P0 — Crítico

- [ ] **P0-GHA-01** Crear workflow de CI (test) en `.github/workflows/ci.yml`.
  - **Archivos afectados:** `.github/workflows/ci.yml`
  - **Riesgo si no se hace:** No hay validación automática antes del deploy.
  - **Criterio de aceptación mínimo:** Cada push/PR a `main` ejecuta `pytest` con cobertura mínima del `85 %`.

### P1 — Necesario

- [ ] **P1-GHA-02** Crear workflow de deploy en `.github/workflows/deploy.yml`.
  - **Archivos afectados:** `.github/workflows/deploy.yml`, `scripts/deploy-server.sh`
  - **Riesgo si no se hace:** El deploy sigue siendo manual y depende de un archivo local con credenciales.
  - **Criterio de aceptación mínimo:** El workflow usa GitHub Secrets, se conecta por SSH con clave privada y ejecuta `scripts/deploy-server.sh` en el VPS.

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

- [ ] **P1-SEO-01** Reducir/fragmentar CSS render-blocking de ~159 KB en `<head>`.
  - *Referencia:* Informe SEO, oportunidad #1.
  - *Nota:* `index.css` pesa ~122 KB e incluye Bootstrap Icons completos + estilos remanentes. Se cargan 6 hojas CSS en serie en el `<head>`.

- [ ] **P1-SEO-02** Diferenciar contenido de páginas dinámicas (localidad e industria) para mitigar thin content y contenido duplicado.
  - *Referencia:* Informe SEO, oportunidad #2.
  - *Nota:* Home, localidades e industrias comparten el mismo template `index.html` con ~90 % de contenido idéntico.

- [ ] **P1-SEO-03** Implementar normalización de URLs en la aplicación (HTTP→HTTPS, trailing slash, www/no-www) o validar que el reverse proxy ya la realice.
  - *Referencia:* Informe SEO, oportunidad #3.
  - *Nota:* Actualmente no hay middleware en FastAPI que redirija a la versión canónica.

### P2 — Mejora

- [ ] **P2-SEO-04** Cambiar `font-display: block` a `swap` (o reemplazar iconos por SVG inline) para eliminar FOIT en Bootstrap Icons.
  - *Referencia:* Informe SEO, oportunidad #4.

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

> Actualizado: los bloqueos de la Etapa 1 ya están resueltos. El deploy manual es funcional.

1. **P1-GHA-02** depende de **P0-GHA-01**: el workflow de deploy debe ejecutarse solo si el workflow de CI pasa.
2. **P1-GHA-03** debe hacerse junto con **P1-GHA-02**: los secrets de GitHub deben estar configurados antes de activar el deploy automático.
3. **P2-GHA-04** depende de **P0-DEV-03**: el rollback automático en GitHub Actions requiere que `scripts/deploy-server.sh` ya tenga rollback implementado.

---

## Notas de implementación

- El entorno de producción ahora usa Python 3.12 compilado en `/usr/local/bin/python3.12`.
- El entorno virtual de producción está en `/var/www/www-datamaq/.venv`.
- El servicio systemd es `datamaq.service`.
- La clave SSH para deploy está en `~/.ssh/datamaq_deploy` (local) y `/home/datamaq/.ssh/authorized_keys` (VPS).
