# Guía de Despliegue Continuo (CD)

## Estado actual

El despliegue es **manual** mediante `scripts/deploy-server.sh`. No existe aún un workflow de GitHub Actions en `.github/workflows/`; su creación está documentada como roadmap en `docs/TODO.md`.

## Configuración del VPS

Se puede automatizar la configuración inicial ejecutando `scripts/setup-vps-user.sh` en el VPS como `root`:

```bash
chmod +x /var/www/datamaq/scripts/setup-vps-user.sh
/var/www/datamaq/scripts/setup-vps-user.sh
```

O seguir los pasos manuales a continuación.

### 1. Usuario dedicado

La aplicación **NO** debe ejecutarse como `root`. Crear un usuario dedicado con shell `bash` y sin contraseña (acceso solo por clave SSH):

```bash
sudo adduser --disabled-password --gecos "" --home /var/www/datamaq datamaq
sudo chown -R datamaq:datamaq /var/www/datamaq
```

> Nota: `setup-vps-user.sh` automatiza este paso y también configura `sudoers`.

### 2. Clonar repositorio

```bash
sudo -u datamaq git clone <URL_DEL_REPOSITORIO> /var/www/datamaq
```

### 3. Entorno virtual e instalación de dependencias

```bash
sudo -u datamaq python3 -m venv /var/www/datamaq/.venv
sudo -u datamaq /var/www/datamaq/.venv/bin/pip install -r /var/www/datamaq/requirements.txt
```

> Nota: el archivo `requirements.txt` está en la raíz del proyecto, no en `backend/`.

### 4. Variables de entorno de la aplicación

Crear `/var/www/datamaq/.env` con los secretos de la app (tokens, IDs de analytics, etc.). Este archivo **no debe versionarse**.

```bash
sudo -u datamaq touch /var/www/datamaq/.env
sudo chmod 600 /var/www/datamaq/.env
```

### 5. Servicio systemd

Crear `/etc/systemd/system/datamaq.service`:

```ini
[Unit]
Description=Datamaq FastAPI Application
After=network.target

[Service]
User=datamaq
Group=datamaq
WorkingDirectory=/var/www/datamaq
ExecStart=/var/www/datamaq/.venv/bin/python3 -m uvicorn src.infrastructure.fastapi.app:app --host 0.0.0.0 --port 8000
Restart=always
EnvironmentFile=/var/www/datamaq/.env

[Install]
WantedBy=multi-user.target
```

Habilitar y arrancar:

```bash
sudo systemctl daemon-reload
sudo systemctl enable datamaq.service
sudo systemctl start datamaq.service
```

### 6. Permisos para reiniciar el servicio (deploy)

El usuario que realiza el deploy necesita reiniciar el servicio. Configurar `sudoers` para que no requiera contraseña:

```bash
echo "datamaq ALL=(ALL) NOPASSWD: /bin/systemctl restart datamaq.service, /bin/systemctl is-active datamaq.service" | sudo tee /etc/sudoers.d/datamaq-deploy
sudo chmod 440 /etc/sudoers.d/datamaq-deploy
```

> `setup-vps-user.sh` automatiza este paso.

## Configuración local del desarrollador

Copiar el template y completar con los datos del VPS:

```bash
cp scripts/.env.deploy.example scripts/.env.deploy
# Editá scripts/.env.deploy con los valores reales
```

Variables obligatorias:

- `DEPLOY_SSH_HOST` — IP o hostname del VPS.
- `DEPLOY_SSH_PORT` — puerto SSH del VPS.
- `DEPLOY_SSH_USER` — usuario dedicado en el VPS (nunca `root`).
- `DEPLOY_REMOTE_DIR` — ruta absoluta del proyecto en el VPS.
- `DEPLOY_SERVICE_NAME` — nombre del servicio systemd (ejemplo: `datamaq.service`).

`scripts/.env.deploy` está en `.gitignore` y **nunca debe commitearse**.

> Nota: `scripts/setup-vps-user.sh` también lee `scripts/.env.deploy` cuando se ejecuta en el VPS. Si el archivo no está presente, usa los valores por defecto (`datamaq`, `/var/www/datamaq`, `datamaq.service`).

## Scripts de deploy

- `scripts/deploy-server.sh` — conecta por SSH al VPS, hace `git pull`, instala dependencias y reinicia el servicio.
- `scripts/view_logs.sh` — muestra los últimos logs del servicio.

## Roadmap hacia GitHub Actions

### Secrets necesarios en el repositorio

Configurar en GitHub: **Settings > Secrets and variables > Actions**.

- `DEPLOY_SSH_HOST` — IP o hostname del VPS.
- `DEPLOY_SSH_PORT` — puerto SSH del VPS.
- `DEPLOY_SSH_USER` — usuario dedicado en el VPS.
- `DEPLOY_SSH_KEY` — clave privada SSH (se recomienda sin frase de paso para CI).

### Workflows planificados

1. `.github/workflows/ci.yml` — ejecutar tests con `pytest` en cada push/PR a `main`.
2. `.github/workflows/deploy.yml` — deploy automático solo si CI pasa, conectándose por SSH al VPS y ejecutando `scripts/deploy-server.sh`.

### Rollback

Implementar en `scripts/deploy-server.sh`:

1. Guardar el commit actual (`HEAD`) antes del `git pull`.
2. Ejecutar health-check HTTP a `http://localhost:8000/` después del reinicio.
3. Si el health-check falla, ejecutar `git reset --hard <commit-previo>` y reiniciar el servicio.

## Notas de seguridad

- No usar `root` para deploy ni ejecución.
- Rotar credenciales SSH si alguna vez estuvieron en un archivo local no cifrado.
- Configurar `PermitRootLogin no` en `/etc/ssh/sshd_config`.
- Mantener `scripts/.env.deploy` fuera del control de versiones.
- Usar autenticación por clave SSH sin frase de paso para CI/CD.

### Configurar acceso SSH por clave

Desde la máquina del desarrollador:

```bash
ssh-keygen -t ed25519 -C "deploy@datamaq" -f ~/.ssh/datamaq_deploy
ssh-copy-id -i ~/.ssh/datamaq_deploy.pub -p 5932 datamaq@168.181.184.103
```

Luego probar:

```bash
ssh -p 5932 -i ~/.ssh/datamaq_deploy datamaq@168.181.184.103
```
- Usar autenticación por clave SSH sin frase de paso para CI/CD.

### Configurar acceso SSH por clave

Desde la máquina del desarrollador:

```bash
ssh-keygen -t ed25519 -C "deploy@datamaq" -f ~/.ssh/datamaq_deploy
ssh-copy-id -i ~/.ssh/datamaq_deploy.pub -p 5932 electricista380@168.181.184.103
```

Luego probar:

```bash
ssh -p 5932 -i ~/.ssh/datamaq_deploy electricista380@168.181.184.103
```
