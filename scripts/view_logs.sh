#!/bin/bash
set -e

# Cargar configuración desde .env.deploy
if [ -f "scripts/.env.deploy" ]; then
    source scripts/.env.deploy
else
    echo "Error: scripts/.env.deploy no encontrado."
    exit 1
fi

echo "Consultando logs remotos en $DEPLOY_SSH_HOST..."

ssh -p $DEPLOY_SSH_PORT $DEPLOY_SSH_USER@$DEPLOY_SSH_HOST "journalctl -u electricista380.service -n 20 --no-pager"
