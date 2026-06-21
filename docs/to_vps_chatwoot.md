# Reporte para Kimi Code - Configuración de Chatwoot en VPS

> Este documento está dirigido al agente de código que opera en la VPS donde corre la instancia de Chatwoot (`https://chatwoot.datamaq.com.ar`). La aplicación FastAPI en `/var/www/datamaq` necesita integrarse con Chatwoot vía Application API.

## Contexto

La web Datamaq (`www-datamaq`) captura leads a través de un formulario de contacto. Queremos que cada lead se sincronice automáticamente como un **Contacto** en Chatwoot.

- **No necesitamos crear conversaciones automáticamente.** El agente iniciará la conversación manualmente desde Chatwoot.
- **Sí necesitamos crear contactos** para que el lead aparezca en la agenda de Chatwoot con nombre, email, teléfono y datos adicionales.

## Qué necesitamos de esta VPS

La aplicación FastAPI necesita estas variables de entorno:

```env
CHATWOOT_BASE_URL=https://chatwoot.datamaq.com.ar
CHATWOOT_ACCOUNT_ID=<id_numérico_de_la_cuenta>
CHATWOOT_API_TOKEN=<token_de_usuario_o_agent_bot>
```

`CHATWOOT_WEBSITE_TOKEN` ya se usa para el widget de chat en el frontend; **no sirve** para la Application API.

## Cómo obtener el Account ID

1. Iniciar sesión en `https://chatwoot.datamaq.com.ar` como administrador.
2. Ir a **Configuración → Cuenta** (o revisar la URL cuando se está dentro de una cuenta, ej. `/app/accounts/1/dashboard`).
3. El número que aparece en la URL es el `CHATWOOT_ACCOUNT_ID`.

Alternativa: desde la consola de Rails en el servidor:

```bash
cd /path/a/chatwoot
RAILS_ENV=production bundle exec rails c
Account.pluck(:id, :name)
```

Anotar el `id` de la cuenta correspondiente a Datamaq.

## Cómo obtener el API Token correcto

**Importante:** no usar Platform API Token. Se necesita un token de **usuario autenticado** (User API Token) o un **Agent Bot Token**.

### Opción A: User API Token (recomendado)

1. Iniciar sesión en Chatwoot con el usuario/agente que atenderá los leads.
2. Ir a **Configuración de perfil → Tokens de acceso**.
3. Generar un nuevo token.
4. Copiar el valor y guardarlo como `CHATWOOT_API_TOKEN`.

### Opción B: Agent Bot Token

Si se prefiere un bot dedicado:

1. Ir a **Configuración → Agent Bots**.
2. Crear un nuevo bot.
3. Copiar el token del bot.

## Permisos necesarios

El usuario/bot asociado al token debe tener acceso al inbox/cuenta donde se van a crear los contactos. Si el token pertenece a un administrador de la cuenta, no debería haber problemas.

## Verificar que el endpoint funciona

Desde esta VPS, ejecutar con las credenciales obtenidas:

```bash
curl -X POST https://chatwoot.datamaq.com.ar/api/v1/accounts/1/contacts \
  -H "Authorization: Bearer <CHATWOOT_API_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@datamaq.com",
    "name": "Test User",
    "phone_number": "+54900000000"
  }'
```

Reemplazar `1` por el `CHATWOOT_ACCOUNT_ID` real.

**Respuesta esperada (éxito):** HTTP 200 con JSON que incluye `payload.contact.id`.

**Respuesta común de error:**

- `401 Unauthorized`: el token es inválido, expiró, o es de Platform API en lugar de User API Token.
- `404 Not Found`: el `account_id` no existe.
- `422 Unprocessable Entity`: faltan campos requeridos en el payload.

## Entregar las credenciales a la aplicación

Una vez confirmado que el `curl` funciona:

1. Editar `/var/www/datamaq/.env` (o el archivo correspondiente en el proyecto FastAPI).
2. Agregar/actualizar:

```env
CHATWOOT_BASE_URL=https://chatwoot.datamaq.com.ar
CHATWOOT_ACCOUNT_ID=<id_obtenido>
CHATWOOT_API_TOKEN=<token_obtenido>
```

3. Reiniciar el servicio `datamaq`:

```bash
sudo systemctl restart datamaq
```

4. Verificar logs:

```bash
sudo journalctl -u datamaq -f
```

Al enviar un lead desde el formulario, se debe ver algo como:

```text
INFO: [ChatwootGatewayHttp] Contacto creado: id=123
```

## Comunicación de vuelta

Si no podés obtener el token o el endpoint no responde, documentar en este archivo o en un mensaje:

1. Versión de Chatwoot instalada (`cat /path/a/chatwoot/.version` o desde UI).
2. Output exacto del `curl` de prueba.
3. Tipo de token que se intentó usar.
4. Si el usuario/bot tiene acceso a la cuenta indicada.
