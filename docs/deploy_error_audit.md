# Informe de Auditoría: Fallo en Despliegue de Código (Git Pull SSH)

Este informe detalla el análisis técnico y diagnóstico de los fallos detectados en el pipeline de GitHub Actions durante la ejecución del script `./scripts/deploy-server.sh`.

---

## 1. Análisis del Error

### Mensaje de Error en Consola (Incidencia 1 - Hostname resolution)
```text
[2026-06-24T14:14:30] Iniciando despliegue de Datamaq en 168.181.184.103...
==> Cambiando a /var/www/www-datamaq
==> Guardando commit actual para posible rollback...
==> Actualizando código...
ssh: Could not resolve hostname github-www-datamaq: Name or service not known
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
Error: Process completed with exit code 1.
```

### Diagnóstico Técnico - Incidencia 1
1. **Lugar de Ejecución:** El error se produce en la máquina remota (**VPS**) durante el paso `==> Actualizando código...`, al ejecutar el comando `git pull` dentro del directorio del proyecto `/var/www/www-datamaq`.
2. **Causa Raíz:** El repositorio clonado en el VPS está configurado para utilizar un alias de Host SSH personalizado para conectarse a GitHub (`git@github-www-datamaq:datamaq-automation/www-datamaq.git`).
3. **El Problema de SSH:** El cliente SSH del VPS no podía resolver el hostname ficticio `github-www-datamaq`. Esto ocurría porque el usuario `datamaq` (cuyo directorio home asignado es `/home/datamaq`) no tenía un archivo de configuración SSH (`/home/datamaq/.ssh/config`) que tradujera el host `github-www-datamaq` a `github.com` ni lo asocie con la clave privada de despliegue correspondiente.
4. **Hallazgo Adicional:** Se localizó la clave privada autorizada del deploy (`id_ed25519_www_datamaq`) y el archivo de alias correspondiente dentro del directorio SSH del usuario `root` (`/root/.ssh/`), pero no estaban disponibles para el usuario `datamaq`.

---

## 2. Acciones Correctivas Aplicadas para la Incidencia 1

Se realizaron las siguientes acciones directamente en el servidor VPS remoto para solucionar de forma permanente la conexión:

### Paso 1: Copiar la Clave de Despliegue al usuario `datamaq`
Copiamos la clave de despliegue original y ajustamos su propiedad y permisos para que SSH la acepte:

```bash
cp /root/.ssh/id_ed25519_www_datamaq /home/datamaq/.ssh/
chown datamaq:datamaq /home/datamaq/.ssh/id_ed25519_www_datamaq
chmod 600 /home/datamaq/.ssh/id_ed25519_www_datamaq
```

### Paso 2: Crear el archivo SSH Config del usuario `datamaq`
Escribimos el archivo de configuración en `/home/datamaq/.ssh/config` para resolver el alias ficticio de GitHub:

```text
Host github-www-datamaq
    HostName github.com
    User git
    IdentityFile /home/datamaq/.ssh/id_ed25519_www_datamaq
    IdentitiesOnly yes
```

```bash
chmod 600 /home/datamaq/.ssh/config
chown datamaq:datamaq /home/datamaq/.ssh/config
```

### Paso 3: Verificación de Conexión Exitosa
Validamos la conexión del usuario de despliegue de forma no interactiva:

```bash
sudo -u datamaq ssh -T -o StrictHostKeyChecking=accept-new git@github-www-datamaq
```

**Resultado obtenido:**
> *"Hi datamaq-automation/www-datamaq! You've successfully authenticated, but GitHub does not provide shell access."*

---

## 3. Segunda Incidencia: Permisos en la Base de Datos Git (`.git/objects`)

Tras corregir el alias SSH, la ejecución de `git pull` arrojó el siguiente error secundario:

```text
error: permisos insuficientes para agregar un objeto a la base de datos del repositorio .git/objects
fatal: failed to write object
fatal: unpack-objects falló
```

### Diagnóstico Técnico - Incidencia 2
Varios archivos y carpetas del repositorio Git (como `index`, `config`, `refs/heads/main` y objetos en `objects/`) pertenecían al usuario `root` u otro usuario del sistema en lugar del dueño del deploy (`datamaq`). Al realizar la descarga de nuevos commits, Git no tenía permisos de escritura para actualizar las referencias y escribir nuevos objetos en disco.

### Acción Correctiva Aplicada
Restablecimos de forma recursiva la propiedad y los permisos de escritura para el usuario `datamaq` en todo el directorio del proyecto en el VPS:

```bash
# Cambiar propiedad recursivamente a datamaq
chown -R datamaq:datamaq /var/www/www-datamaq

# Asegurar permisos de lectura, escritura y búsqueda en directorios para el dueño
chmod -R u+rwX /var/www/www-datamaq
```

### Verificación de git pull exitosa
Ejecutamos un `git pull` de prueba en el VPS bajo el contexto del usuario `datamaq`:

```bash
sudo -u datamaq git -C /var/www/www-datamaq pull
```

**Resultado obtenido:**
El repositorio se actualizó correctamente mediante un fast-forward estable, confirmando la resolución definitiva de ambas incidencias de acceso y permisos. El flujo de GitHub Actions se encuentra ahora **completamente desbloqueado y operativo**.
