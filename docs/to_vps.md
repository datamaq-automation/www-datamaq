# Configuración de Permisos Sudoers para Despliegue Automático en VPS

Este documento contiene las instrucciones y comandos necesarios para que el agente del VPS configure los privilegios de `sudo` requeridos para reiniciar el servicio de Datamaq de manera no interactiva.

## Contexto
El script de despliegue continuo `deploy-server.sh` falla durante el reinicio de la aplicación con el siguiente mensaje de error:
`sudo: a terminal is required to read the password; either use the -S option to read from standard input or configure an askpass helper`

Esto se debe a que el comando `sudo systemctl restart` requiere privilegios de superusuario y no tiene habilitada la opción de ejecución sin contraseña (`NOPASSWD`).

---

## Instrucciones de Resolución Autónoma (para el Agente en el VPS)

Para evitar la edición interactiva de `/etc/sudoers`, se recomienda crear un archivo de configuración dedicado dentro del directorio `/etc/sudoers.d/`. El nombre del usuario y el servicio se pueden resolver de forma dinámica.

### Paso 1: Identificar las Variables del Entorno
Ejecutá los siguientes comandos para definir las variables locales en tu terminal:
```bash
# 1. Obtener el nombre del usuario actual que realiza el deploy
DEPLOY_USER=$(whoami)

# 2. Buscar el nombre del servicio systemd de la aplicación
# Si conocés el nombre exacto (por ejemplo: datamaq.service), definilo directamente:
SERVICE_NAME="datamaq.service"

# O buscalo dinámicamente si no estás seguro:
# SERVICE_NAME=$(systemctl list-units --type=service --all | grep -i "datamaq" | awk '{print $1}' | head -n 1)
```

### Paso 2: Crear y Validar el Archivo Sudoers Temporal
Creá una regla de sudoers en una ubicación temporal para comprobar que su sintaxis sea correcta antes de instalarla (esto previene dejar al sistema sin acceso root por un error tipográfico):

```bash
# Crear el archivo temporal con los permisos NOPASSWD específicos
echo "$DEPLOY_USER ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart $SERVICE_NAME, /usr/bin/systemctl is-active $SERVICE_NAME" > /tmp/datamaq-deploy-sudoers

# Validar la sintaxis del archivo temporal con visudo
sudo visudo -c -f /tmp/datamaq-deploy-sudoers
```

> [!IMPORTANT]
> Si el comando `visudo -c` retorna un error, **no continúes**. Corrige la sintaxis del archivo temporal antes de moverlo.

### Paso 3: Instalar la Regla en `/etc/sudoers.d/`
Si la validación fue exitosa, mové el archivo al directorio seguro con los permisos restrictivos requeridos por el sistema (`0440`):

```bash
# Mover el archivo a la carpeta de configuración de sudoers
sudo mv /tmp/datamaq-deploy-sudoers /etc/sudoers.d/datamaq-deploy

# Aplicar los permisos seguros requeridos (lectura exclusiva de root)
sudo chmod 0440 /etc/sudoers.d/datamaq-deploy
sudo chown root:root /etc/sudoers.d/datamaq-deploy
```

### Paso 4: Validar Funcionamiento
Comprobá que el comando se ejecute sin pedir contraseña ejecutando el comando de estado desde tu usuario actual:
```bash
sudo systemctl is-active "$SERVICE_NAME"
```
Si el comando devuelve `active` (o `inactive`) de forma inmediata sin solicitar contraseña, la configuración se completó de manera exitosa.
