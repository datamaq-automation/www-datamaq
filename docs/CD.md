# Guía de Despliegue Continuo (CD)

El proyecto cuenta con un flujo de despliegue automático hacia el VPS.

## Configuración de GitHub Secrets
Para activar el CD, configura los siguientes secretos en tu repositorio (Settings > Secrets and variables > Actions):
 - `SSH_HOST`: IP de tu VPS.
 - `SSH_PRIVATE_KEY`: Llave privada SSH (con acceso `root` al VPS, necesaria para los comandos de `systemctl` y `chown` iniciales, aunque la aplicación se ejecuta con un usuario sin
      privilegios).

 ## Configuración Inicial en el VPS (PASOS MANUALES OBLIGATORIOS, UNA SOLA VEZ)

 **¡IMPORTANTE!: La aplicación NO debe ejecutarse como usuario `root`. Debemos crear un usuario dedicado sin privilegios para mayor seguridad.**

 1.  **Crear Usuario Dedicado para la Aplicación (ej. `electricista380`):**
      sudo adduser --system --no-create-home electricista380
  Si prefieres un usuario con shell y directorio home para depuración, usa:
  sudo adduser electricista380_user

2.  **Crear Directorio del Proyecto y Clonar Repositorio:**
      sudo mkdir -p /var/www/electricista380
      sudo chown -R electricista380:electricista380 /var/www/electricista380
      cd /var/www/electricista380
      git clone {URL_DEL_REPOSITORIO_GIT_DE_ESTE_PROYECTO} .

     *(Reemplaza `{URL_DEL_REPOSITORIO_GIT_DE_ESTE_PROYECTO}` con la URL real de tu repositorio).*

3.  **Crear Entorno Virtual e Instalar Dependencias:**
      python3 -m venv .venv
      /var/www/electricista380/.venv/bin/pip install -r backend/requirements.txt # Ajusta la ruta si requirements.txt no está en 'backend/'


4.  **Crear y Configurar Archivo `.env` (SECRETS):**
      touch /var/www/electricista380/.env
  Luego edita este archivo con tus variables de entorno y secretos.

     **Este archivo NO debe ser versionado en Git.**

5.  **Configurar Servicio Systemd (`/etc/systemd/system/electricista380.service`):**
     Crea un archivo con el siguiente contenido:
      [Unit]
      Description=Datamaq FastAPI Application
      After=network.target

      [Service]
      User=electricista380  # El usuario sin privilegios creado
      Group=electricista380 # El grupo sin privilegios
      WorkingDirectory=/var/www/electricista380
      ExecStart=/var/www/electricista380/.venv/bin/python3 -m uvicorn src.infrastructure.fastapi.app:app --host 0.0.0.0 --port 8000
      Restart=always
      EnvironmentFile=/var/www/electricista380/.env

      [Install]
      WantedBy=multi-user.target
     Después de crear este archivo, ejecuta los siguientes comandos para habilitar y arrancar el servicio:
      sudo systemctl enable electricista380.service
      sudo systemctl start electricista380.service


## Flujo de Despliegue Automatizado
1.  El despliegue se dispara automáticamente al hacer push a la rama `main`.
2.  GitHub Actions se conecta vía SSH al VPS usando las credenciales configuradas.
3.  Se ejecuta `scripts/deploy-server.sh` en el servidor (ubicado en `/var/www/electricista380`).
4.  El script se encarga de:
     *   Hacer `git pull origin main` para obtener los últimos cambios.
     *   Actualizar las dependencias de Python si es necesario.
     *   Realizar el "cache busting" del frontend.
     *   Reiniciar el servicio `electricista380.service` para aplicar los cambios.
