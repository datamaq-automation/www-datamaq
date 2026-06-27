# Guía de Despliegue en Producción

Esta guía detalla el proceso de preparación del servidor VPS, la configuración de los servicios del sistema (Systemd, Nginx) y el flujo de despliegue automatizado para la aplicación **www-datamaq**.

---

## 1. Configuración de Variables de Despliegue

Tanto para la preparación inicial como para las tareas de despliegue y visualización de logs, se debe crear el archivo de configuración en tu entorno local:

```bash
cp scripts/.env.deploy.example scripts/.env.deploy
```

Edita el archivo [scripts/.env.deploy](file:///home/agustin/proyectos_software/www-datamaq/scripts/.env.deploy) con los valores correspondientes del servidor:
* `DEPLOY_SSH_HOST`: IP o dominio del servidor VPS.
* `DEPLOY_SSH_PORT`: Puerto de conexión SSH (habitualmente 22).
* `DEPLOY_SSH_USER`: Usuario del sistema dedicado al servicio (ej. `datamaq`).
* `DEPLOY_REMOTE_DIR`: Ruta absoluta en el VPS donde se clonará el código (ej. `/var/www/datamaq`).
* `DEPLOY_SERVICE_NAME`: Nombre del servicio del sistema en systemd (ej. `datamaq.service`).

---

## 2. Preparación Inicial del VPS (Bootstrap)

Para preparar el servidor de producción con un usuario y permisos seguros, ejecuta el script de aprovisionamiento. **Este script debe correr en el VPS como usuario `root`**:

1. Copia el script [setup-vps-user.sh](file:///home/agustin/proyectos_software/www-datamaq/scripts/setup-vps-user.sh) al servidor y ejecútalo como root:
   ```bash
   sudo ./setup-vps-user.sh
   ```
2. Este script se encargará de:
   * Crear el usuario dedicado para la aplicación (`datamaq` por defecto) de forma segura (sin acceso por contraseña, solo SSH keys).
   * Crear el directorio remoto asignándole la propiedad al usuario dedicado.
   * Configurar los permisos de `sudoers` para permitirle al usuario del despliegue reiniciar e inspeccionar el estado del servicio systemd sin ingresar contraseña.

---

## 3. Configuración del Servicio Systemd (`datamaq.service`)

En el VPS, crea el archivo de servicio de la aplicación en la ruta `/etc/systemd/system/datamaq.service` (reemplaza `datamaq` y las rutas si utilizas valores personalizados):

```ini
[Unit]
Description=Servicio Web Datamaq (FastAPI)
After=network.target

[Service]
User=datamaq
Group=datamaq
WorkingDirectory=/var/www/datamaq
ExecStart=/var/www/datamaq/.venv/bin/python3 -m uvicorn src.infrastructure.fastapi.app:app --host 127.0.0.1 --port 8000
EnvironmentFile=/var/www/datamaq/.env
Restart=always
RestartSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Habilita e inicia el servicio en el VPS:
```bash
sudo systemctl daemon-reload
sudo systemctl enable datamaq.service
sudo systemctl start datamaq.service
```

---

## 4. Configuración del Proxy Inverso (Nginx)

Para exponer la aplicación en producción de manera segura (puertos 80 y 443), utiliza **Nginx** como proxy inverso frente a Uvicorn.

Crea un archivo de configuración de bloque de servidor en `/etc/nginx/sites-available/datamaq` en el VPS:

```nginx
server {
    listen 80;
    server_name datamaq.com.ar www.datamaq.com.ar;

    # Redirección a HTTPS (Recomendado para producción)
    # return 301 https://$host$request_uri;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Optimización opcional para archivos estáticos
    location /static/ {
        alias /var/www/datamaq/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
}
```

Habilita el sitio y reinicia Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/datamaq /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

> [!NOTE]
> Para habilitar HTTPS (SSL), puedes utilizar **Certbot** para obtener e instalar automáticamente un certificado de Let's Encrypt ejecutando: `sudo certbot --nginx -d datamaq.com.ar -d www.datamaq.com.ar`.

---

## 5. Proceso de Despliegue Automatizado

Una vez configurado el entorno, todo cambio realizado en la rama principal se sube al servidor ejecutando el script localmente desde tu máquina de desarrollo o entorno de CI/CD:

```bash
./scripts/deploy-server.sh
```

### Flujo del script y Rollback Automático:
1. **Paso por SSH:** Se conecta al VPS de forma segura mediante el usuario del despliegue (no root).
2. **Copia de Respaldo (Rollback Point):** Guarda el hash del commit actual en el servidor antes de realizar cambios.
3. **Actualización:** Realiza un `git pull` en la carpeta del servidor para obtener los últimos cambios.
4. **Dependencias:** Ejecuta `pip install` sobre el entorno virtual del servidor (`.venv`) si hay cambios en `requirements.txt`.
5. **Reinicio:** Reinicia el servicio `systemd` para aplicar los cambios de código.
6. **Health Check:** Realiza peticiones HTTP locales en el VPS a `http://localhost:8000/` durante un máximo de 30 segundos.
   * **Si responde HTTP 200:** El despliegue finaliza de manera exitosa.
   * **Si falla o supera el tiempo límite:** Revierte automáticamente el repositorio al commit anterior guardado (`git reset --hard`) y vuelve a reiniciar el servicio estable, previniendo caídas del sitio.

---

## 6. Monitoreo y Diagnóstico Remoto

Puedes visualizar la salida de logs remotos de la aplicación directamente desde la máquina local sin necesidad de loguearte interactivamente por SSH:

```bash
./scripts/view_logs.sh
```
Este comando consulta y muestra las últimas 20 líneas del servicio en tiempo real a través de `journalctl`.
