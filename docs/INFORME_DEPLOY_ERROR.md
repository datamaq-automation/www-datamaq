# Informe de Incidente: Error en el Despliegue (Permisos `.git/objects`)

- **Fecha del incidente:** 2026-08-05
- **Ruta de código afectada:** `scripts/deploy-server.sh`
- **Tipo:** Despliegue fallido en VPS (producción)
- **Clasificación:** Problema de infraestructura (VPS), **no** un defecto del código de la aplicación

---

## 1. Resumen Ejecutivo

El despliegue automatizado hacia el VPS falló durante el paso de actualización del código (`git pull`). El error no se debe a cambios en el repositorio ni a lógica de la aplicación, sino a **permisos insuficientes del usuario de despliegue sobre la base de objetos de Git** (`.git/objects`) en el servidor remoto.

El usuario con el que se ejecuta el script no tiene permiso de escritura sobre el directorio `.git/objects` del repositorio en `/var/www/www-***`, por lo que Git no puede registrar los objetos entrantes del `pull`.

---

## 2. Síntoma / Log del Error

Salida del script `./scripts/deploy-server.sh`:

```
[2026-08-05T02:57:17] Iniciando despliegue de Datamaq en ***...
==> Cambiando a /var/www/www-***
==> Guardando commit actual para posible rollback...
==> Actualizando código...
error: insufficient permission for adding an object to repository database .git/objects
fatal: failed to write object
fatal: unpack-objects failed
Error: Process completed with exit code 1.
```

El proceso termina con código de salida `1` y **no** se ejecuta el `git pull` (scripts/deploy-server.sh:45), por lo que no se instalan dependencias, no se reinicia el servicio y no se dispara el rollback (el código en el servidor permanece intacto).

---

## 3. Análisis de Causa Raíz

### 3.1 Dónde falla exactamente

El fallo ocurre en el paso `git pull` dentro del bloque remoto del script (scripts/deploy-server.sh:45). Ninguna parte de la lógica de la aplicación está involucrada.

### 3.2 Causa inmediata

Git no puede escribir los objetos recibidos en la base de objetos local del repositorio. El mensaje `error: insufficient permission for adding an object to repository database .git/objects` indica que el usuario del despliegue (definido por `DEPLOY_SSH_USER`) no tiene permisos de escritura sobre:

```
$DEPLOY_REMOTE_DIR/.git/objects
```

### 3.3 Causa raíz probable

El repositorio en el VPS quedó con archivos propiedad de un usuario distinto al de despliegue. El escenario típico:

1. El directorio de la aplicación se creó o el repo se clonó/inicializó con `root` (o con otro usuario).
2. Los archivos de `.git/` (incluyendo `.git/objects`) quedaron con ese ownership.
3. Al ejecutar el deploy como el usuario dedicado, Git no puede escribir en `.git/objects`.

Esto es consistente con la recomendación de la [Guía de Despliegue](CD.md#2-preparación-inicial-del-vps-bootstrap): el script `setup-vps-user.sh` debe asignar la propiedad del directorio remoto al usuario dedicado; si la preparación inicial no se realizó con él (o se clonó como `root` antes), se produce este síntoma.

---

## 4. Diagnóstico en el VPS

Conectarse al VPS y ejecutar los siguientes comandos para confirmar:

```bash
whoami
ls -ld /var/www/www-***
ls -ld /var/www/www-***/.git
ls -ld /var/www/www-***/.git/objects
```

Si el `owner` de `.git/objects` (o de directorios superiores) no corresponde al usuario del despliegue, se confirma la causa raíz.

---

## 5. Pasos de Resolución (en el VPS)

### 5.1 Corregir el ownership del repositorio

Como `root` (o vía `sudo`), asignar la propiedad al usuario dedicado del despliegue:

```bash
sudo chown -R <usuario_despliegue>:<grupo_despliegue> /var/www/www-***
```

> [!NOTE]
> Si el servicio systemd corre con otro usuario, verificar si ese usuario necesita escritura sobre algún subdirectorio (por ejemplo, datos generados). En tal caso puede usarse un grupo compartido en lugar de un único owner.

### 5.2 Verificar la corrección

Comprobar que el usuario del despliegue puede escribir sobre la base de objetos y que el repo está sano:

```bash
cd /var/www/www-***
touch .git/objects/.writetest && rm .git/objects/.writetest
sudo -u <usuario_despliegue> git status
```

### 5.3 Reintentar el despliegue

Ejecutar nuevamente desde la máquina local:

```bash
./scripts/deploy-server.sh
```

> [!IMPORTANT]
> Según las reglas del proyecto, el despliegue a producción debe ser explícitamente aprobado por el usuario.

---

## 6. Prevención Futura

Se recomienda añadir al inicio del bloque remoto de `scripts/deploy-server.sh` una verificación previa de escritura sobre el repositorio git que emita un mensaje claro antes de intentar el `pull`. Esta verificación detecta cualquier archivo o directorio no escribible dentro de `.git` (index, HEAD, objects):

```bash
echo "==> Verificando permisos de escritura sobre el repositorio git..."
NOT_WRITABLE=$(find .git -maxdepth 2 ! -writable 2>/dev/null | head -1)
if [ -n "$NOT_WRITABLE" ]; then
    echo "ERROR: Sin permiso de escritura en '$NOT_WRITABLE'."
    echo "Corregí el ownership del repositorio en el VPS:"
    echo "  sudo chown -R <usuario_despliegue>:<grupo> $DEPLOY_REMOTE_DIR"
    exit 1
fi
```

Esto convierte un error críptico de Git en un diagnóstico accionable en futuros despliegues.

---

## 7. Registro del Incidente

| Campo          | Detalle                                        |
|----------------|------------------------------------------------|
| Fecha          | 2026-08-05                                     |
| Entorno        | VPS de producción (`DEPLOY_REMOTE_DIR`)        |
| Comando        | `./scripts/deploy-server.sh`                   |
| Paso fallido   | `git pull` (scripts/deploy-server.sh:45)       |
| Código de error| `unpack-objects failed` (exit code 1)          |
| Causa raíz     | Permisos de escritura insuficientes sobre `.git/objects` en el VPS |
| Impacto        | Nulo sobre la aplicación: el código en el servidor no cambió ni se reinició el servicio |
| Resolución     | Corrección de ownership del repositorio al usuario del despliegue (sección 5) |
