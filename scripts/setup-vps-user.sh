#!/bin/bash
set -e

# Script de bootstrap para ejecutar EN EL VPS como root.
# No ejecutar en la máquina de desarrollo local.

if [ "$(id -u)" -ne 0 ]; then
    echo "Error: este script debe ejecutarse como root en el VPS."
    echo "En tu máquina local no tenés permisos para crear usuarios del sistema."
    exit 1
fi

# Cargar configuración desde .env.deploy si existe; usar defaults seguros si no.
if [ -f "scripts/.env.deploy" ]; then
    source scripts/.env.deploy
fi

APP_USER="${DEPLOY_SSH_USER:-electricista380}"
APP_DIR="${DEPLOY_REMOTE_DIR:-/var/www/electricista380}"
SERVICE="${DEPLOY_SERVICE_NAME:-electricista380.service}"

echo "==> Configuración: usuario=$APP_USER, directorio=$APP_DIR, servicio=$SERVICE"

echo "==> Creando usuario $APP_USER..."
if id "$APP_USER" &>/dev/null; then
    echo "El usuario $APP_USER ya existe. Asegurando shell y home..."
    usermod -s /bin/bash "$APP_USER"
else
    # Usuario normal con home y shell bash, sin contraseña (login solo por SSH key).
    adduser --disabled-password --gecos "" --home "$APP_DIR" "$APP_USER"
fi

echo "==> Asegurando permisos de $APP_DIR..."
mkdir -p "$APP_DIR"
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

echo "==> Configurando sudoers para reiniciar el servicio..."
cat > "/etc/sudoers.d/$APP_USER-deploy" <<EOF
$APP_USER ALL=(ALL) NOPASSWD: /bin/systemctl restart $SERVICE
$APP_USER ALL=(ALL) NOPASSWD: /bin/systemctl is-active $SERVICE
$APP_USER ALL=(ALL) NOPASSWD: /bin/systemctl status $SERVICE
EOF
chmod 440 "/etc/sudoers.d/$APP_USER-deploy"

echo "==> Asegurando que el servicio $SERVICE use el usuario $APP_USER..."
if [ -f "/etc/systemd/system/$SERVICE" ]; then
    sed -i "s/^User=.*/User=$APP_USER/" "/etc/systemd/system/$SERVICE"
    sed -i "s/^Group=.*/Group=$APP_USER/" "/etc/systemd/system/$SERVICE"
    systemctl daemon-reload
    systemctl restart "$SERVICE"
else
    echo "ADVERTENCIA: No se encontró /etc/systemd/system/$SERVICE"
    echo "Creá el archivo manualmente según docs/CD.md"
fi

echo "==> Configuración completada."
echo "Verificá que el servicio esté activo con: sudo systemctl is-active $SERVICE"
echo ""
echo "Para habilitar deploy por SSH, agregá la clave pública del desarrollador a:"
echo "  $APP_DIR/.ssh/authorized_keys"
