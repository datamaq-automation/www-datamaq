#!/bin/bash
set -e

# Cargar configuración desde .env.deploy
if [ -f "scripts/.env.deploy" ]; then
    source scripts/.env.deploy
else
    echo "Error: scripts/.env.deploy no encontrado."
    echo "Copiá scripts/.env.deploy.example a scripts/.env.deploy y completá los valores."
    exit 1
fi

# Validaciones mínimas
if [ -z "$DEPLOY_SSH_HOST" ] || [ -z "$DEPLOY_SSH_PORT" ] || [ -z "$DEPLOY_SSH_USER" ] || [ -z "$DEPLOY_REMOTE_DIR" ] || [ -z "$DEPLOY_SERVICE_NAME" ]; then
    echo "Error: faltan variables en scripts/.env.deploy."
    echo "Copiá scripts/.env.deploy.example a scripts/.env.deploy y completá los valores."
    exit 1
fi

if [ "$DEPLOY_SSH_USER" = "root" ]; then
    echo "Error: no se permite desplegar como root. Usá un usuario dedicado."
    exit 1
fi

# Función de log local
log() { echo "[$(date +"%Y-%m-%dT%H:%M:%S")] $1"; }

log "Iniciando despliegue de Datamaq en $DEPLOY_SSH_HOST..."

# Ejecutamos los comandos remotos uno por uno para evitar problemas de parsing en la cadena
ssh -T -p "$DEPLOY_SSH_PORT" "$DEPLOY_SSH_USER@$DEPLOY_SSH_HOST" << EOF
    set -e
    echo "==> Cambiando a $DEPLOY_REMOTE_DIR"
    cd "$DEPLOY_REMOTE_DIR" || { echo "Error: no se pudo entrar a $DEPLOY_REMOTE_DIR"; exit 1; }

    echo "==> Actualizando código..."
    git pull

    echo "==> Instalando dependencias..."
    ./.venv/bin/pip install -r requirements.txt

    echo "==> Reiniciando servicio $DEPLOY_SERVICE_NAME..."
    sudo systemctl restart "$DEPLOY_SERVICE_NAME"

    echo "==> Verificando salud del servicio..."
    sleep 2
    sudo systemctl is-active "$DEPLOY_SERVICE_NAME"
EOF

if [ $? -eq 0 ]; then
    log "Despliegue exitoso."
else
    log "ERROR: El despliegue falló."
    exit 1
fi
