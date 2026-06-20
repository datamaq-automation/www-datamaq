#!/bin/bash
set -e

# Cargar configuración desde .env.deploy
if [ -f "scripts/.env.deploy" ]; then
    source scripts/.env.deploy
else
    echo "Error: scripts/.env.deploy no encontrado. Copiá scripts/.env.deploy.example y completá los valores."
    exit 1
fi

# Validaciones mínimas
if [ -z "$DEPLOY_SSH_HOST" ] || [ -z "$DEPLOY_SSH_PORT" ] || [ -z "$DEPLOY_SSH_USER" ] || [ -z "$DEPLOY_REMOTE_DIR" ]; then
    echo "Error: faltan variables en scripts/.env.deploy."
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
ssh -p "$DEPLOY_SSH_PORT" "$DEPLOY_SSH_USER@$DEPLOY_SSH_HOST" << EOF
    set -e
    cd "$DEPLOY_REMOTE_DIR"
    echo "Actualizando código..." && git pull
    echo "Instalando dependencias..." && ./.venv/bin/pip install -r requirements.txt
    echo "Reiniciando servicio..." && sudo systemctl restart electricista380.service
    echo "Verificando salud del servicio..." && sleep 2 && sudo systemctl is-active electricista380.service
EOF

if [ $? -eq 0 ]; then
    log "Despliegue exitoso."
else
    log "ERROR: El despliegue falló."
    exit 1
fi
