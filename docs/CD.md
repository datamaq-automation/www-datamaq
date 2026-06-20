# Guía de Despliegue Continuo (CD)

## Estado actual

El despliegue es **manual** mediante `scripts/deploy-server.sh`. No existe aún un workflow de GitHub Actions en `.github/workflows/`; su creación está documentada como roadmap en `docs/TODO.md`.

## Configuración del VPS

Se puede automatizar la configuración inicial ejecutando `scripts/setup-vps-user.sh` en el VPS como `root`:

```bash
chmod +x /var/www/electricista380/scripts/setup-vps-user.sh
/var/www/electricista380/scripts/setup-vps-user.sh
```

O seguir los pasos manuales a continuación.

### 1. Usuario dedicado

La aplicación **NO** debe ejecutarse como `root`. Crear un usuario dedicado:

```bash
sudo adduser --system --group --home /var/www/electricista380 electricista380
sudo chown -R electricista380:electricista380 /var/www/electricista380
```

### 2. Clonar repositorio

```bash
sudo -u electricista380 git clone <URL_DEL_REPOSITORIO> /var/www/electricista380
```

### 3. Entorno virtual e instalación de dependencias

```bash
sudo -u electricista380 python3 -m venv /var/www/electricista380/.venv
sudo -u electricista380 /var/www/electricista380/.venv/bin/pip install -r /var/www/electricista380/requirements.txt
```

> Nota: el archivo `requirements.txt` está en la raíz del proyecto, no en `backend/`.

### 4. Variables de entorno de la aplicación

Crear `/var/www/electricista380/.env` con los secretos de la app (tokens, IDs de analytics, etc.). Este archivo **no debe versionarse**.

```bash
sudo -u electricista380 touch /var/www/electricista380/.env
sudo chmod 600 /var/www/electricista380/.env
```

### 5. Servicio systemd

Crear `/etc/systemd/system/electricista380.service`:

```ini
[Unit]
Description=Datamaq FastAPI Application
After=network.target

[Service]
User=electricista380
Group=electricista380
WorkingDirectory=/var/www/electricista380
ExecStart=/var/www/electricista380/.venv/bin/python3 -m uvicorn src.infrastructure.fastapi.app:app --host 0.0.0.0 --port 8000
Restart=always
EnvironmentFile=/var/www/electricista380/.env

[Install]
WantedBy=multi-user.target
```

Habilitar y arrancar:

```bash
sudo systemctl daemon-reload
sudo systemctl enable electricista380.service
sudo systemctl start electricista380.service
```

### 6. Permisos para reiniciar el servicio (deploy)

El usuario que realiza el deploy necesita reiniciar el servicio. Configurar `sudoers` para que no requiera contraseña:

```bash
echo "electricista380 ALL=(ALL) NOPASSWD: /bin/systemctl restart electricista380.service, /bin/systemctl is-active electricista380.service" | sudo tee /etc/sudoers.d/electricista380-deploy
sudo chmod 440 /etc/sudoers.d/electricista380-deploy
```

## Configuración local del desarrollador

Copiar el template y completar con los datos del VPS:

```bash
cp scripts/.env.deploy.example scripts/.env.deploy
```

`scripts/.env.deploy` está en `.gitignore` y **nunca debe commitearse**.

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
