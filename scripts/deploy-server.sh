#!/bin/bash
set -e
echo "Iniciando despliegue..."
cd /root/fitba_impacto_economico
git pull origin main
./.venv/bin/pip install -r backend/requirements.txt
TIMESTAMP=$(date +%s)
sed -i "s/v=[0-9]*/v=$TIMESTAMP/g" backend/frontend/index.html
systemctl restart fitba-impacto-economico.service
echo "Despliegue exitoso."
