#!/bin/bash
set -e

# Cargar configuración desde .env.deploy
if [ -f "scripts/.env.deploy" ]; then
    source scripts/.env.deploy
else
    echo "Error: scripts/.env.deploy no encontrado."
    exit 1
fi

# Función de log local
log() { echo "[$(date +"%Y-%m-%dT%H:%M:%S")] $1"; }

log "Iniciando despliegue de Electricista 380 en $DEPLOY_SSH_HOST..."

# Ejecutamos los comandos remotos uno por uno para evitar problemas de parsing en la cadena
ssh -p $DEPLOY_SSH_PORT $DEPLOY_SSH_USER@$DEPLOY_SSH_HOST << EOF
    cd $DEPLOY_REMOTE_DIR
    echo "Actualizando código..." && git pull
    echo "Instalando dependencias..." && ./venv/bin/pip install -r requirements.txt
    echo "Reiniciando servicio..." && systemctl restart electricista380.service
    echo "Verificando salud del servicio..." && sleep 2 && systemctl is-active electricista380.service
EOF

if [ $? -eq 0 ]; then
    log "Despliegue exitoso."
else
    log "ERROR: El despliegue falló."
    exit 1
fi
