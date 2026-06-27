# Auditoría SEO Técnica / DevOps / Performance — `datamaq.com.ar`

> **Fecha de auditoría:** 2026-06-27  
> **Entorno:** FastAPI + Jinja2 SSR en VPS AlmaLinux, Nginx como reverse proxy, Cloudflare en modo proxy.  
> **Restricción respetada:** no se ejecutó ningún cambio en Nginx. Solo se recopilaron evidencias y se proponen comandos/scripts para aplicar tras backup.

---

## 1. Resumen ejecutivo

| Hallazgo | Severidad |
|---|---|
| `HEAD /` devuelve `405` con `X-Robots-Tag: noindex, nofollow` (tanto por Cloudflare como contra el origen). `GET /` está OK, pero esto puede confundir crawlers y herramientas de auditoría. | **Alta** |
| No hay header `Strict-Transport-Security` (HSTS). | Media |
| No hay `Content-Security-Policy`. | Media |
| Nginx origen no comprime (`gzip`/`brotli`); Cloudflare sí lo hace en el edge. | Baja/Media |
| Redirección `/courses/* → /cursos` es genérica y pierde la URL específica de cada curso/lección. | Media |
| `/instructor/agustinbustos/` devuelve `404` en lugar de redirigir a la nueva URL. | Alta |
| Core Web Vitals de navegación no pudieron medirse por falta de Lighthouse/Chrome en el servidor. | — |

---

## 2. Configuración de Nginx analizada

Archivos relevantes:

```bash
/etc/nginx/nginx.conf
/etc/nginx/conf.d/datamaq.conf
/etc/nginx/conf.d/security-headers-common.conf
```

### `datamaq.conf` (origen)

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name datamaq.com.ar www.datamaq.com.ar;
    location ^~ /.well-known/acme-challenge/ { ... }
    location / { return 301 https://datamaq.com.ar$request_uri; }
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name datamaq.com.ar www.datamaq.com.ar;

    ssl_certificate /etc/letsencrypt/live/datamaq.com.ar/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/datamaq.com.ar/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    include /etc/nginx/conf.d/security-headers-common.conf;

    location ~ ^/courses {
        return 301 https://datamaq.com.ar/cursos;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;
        proxy_read_timeout 60s;
    }
}
```

### `security-headers-common.conf`

```nginx
server_tokens off;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=(), payment=()" always;
```

> Nota: la última línea contiene un `\r` (carriage return) al final. No es crítico, pero conviene normalizar el archivo.

---

## 3. Resultados por categoría

### 3.1 Servidor / Nginx

| Item | Estado actual | Severidad | Impacto SEO | Corrección propuesta |
|---|---|---|---|---|
| **Proxy a FastAPI** | `proxy_pass http://127.0.0.1:8000` | — | — | OK |
| **HTTP/2** | ALPN negocia `h2` tanto en Cloudflare como contra el origen. | — | Positivo | OK |
| **HTTP/3** | Anunciado vía `alt-svc: h3=":443"; ma=86400` por Cloudflare. | — | Positivo | OK |
| **Compresión en origen** | `gzip` no está habilitado en Nginx. Cloudflare entrega `content-encoding: gzip/br` en el edge. | Media | Si alguna petición bypass Cloudflare o se purga caché, el origen envía bytes sin comprimir. | Agregar en `/etc/nginx/nginx.conf` dentro de `http { ... }` (ver script abajo). |
| **Cache de estáticos** | Assets con `Cache-Control: public, max-age=604800, immutable`. HTML con `cf-cache-status: DYNAMIC`. | — | Correcto | OK |
| **`X-Robots-Tag` en HEAD** | `HEAD /` (y cualquier HEAD a ruta SSR) devuelve `405` + `X-Robots-Tag: noindex, nofollow`. `GET` no lo tiene. | Alta | Puede hacer que algunos crawlers/probes interpreten que todo está bloqueado. Genera ruido en auditorías. | Corregir en FastAPI para que `HEAD` sea manejado igual que `GET` o para que no se envíe `X-Robots-Tag` en respuestas 405. |
| **`server_tokens`** | `off` | — | — | OK |

**Script para habilitar gzip en origen (aplicar tras backup):**

```bash
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak-$(date +%Y%m%d-%H%M%S)
sudo nano /etc/nginx/nginx.conf
```

Dentro del bloque `http { ... }` agregar:

```nginx
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 5;
gzip_min_length 256;
gzip_types
    text/plain
    text/css
    text/xml
    application/json
    application/javascript
    application/xml+rss
    application/atom+xml
    image/svg+xml;
```

Luego:

```bash
sudo nginx -t && sudo systemctl reload nginx
```

---

### 3.2 SSL / TLS

| Item | Estado actual | Severidad | Impacto SEO | Corrección propuesta |
|---|---|---|---|---|
| **Certificado Cloudflare (usuario)** | Válido. `CN=datamaq.com.ar`, emisor Google Trust Services, expira **2026-09-07**. | — | — | OK |
| **Certificado origen (Let's Encrypt)** | Válido. `CN=datamaq.com.ar`, emisor Let's Encrypt YR1, expira **2026-09-17**. | — | — | OK |
| **TLS mínimo** | TLSv1.3 contra origen y Cloudflare. | — | Positivo | OK |
| **HSTS** | No se envía `Strict-Transport-Security`. | Media | Menor impacto directo en rankings, pero es requisito de seguridad y evita downgrade. | Agregar header HSTS. |

**Script propuesto para HSTS (origen):**

```bash
sudo cp /etc/nginx/conf.d/security-headers-common.conf \
        /etc/nginx/conf.d/security-headers-common.conf.bak-$(date +%Y%m%d-%H%M%S)
sudo nano /etc/nginx/conf.d/security-headers-common.conf
```

Agregar:

```nginx
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
```

> ⚠️ Antes de agregar `preload`, validar que todas las subpropiedades sirvan siempre HTTPS. Si no se quiere preload, omitir esa palabra.

---

### 3.3 Redirecciones

| Item | Estado actual | Severidad | Impacto SEO | Corrección propuesta |
|---|---|---|---|---|
| **HTTP → HTTPS** | `301` a `https://datamaq.com.ar/` | — | — | OK |
| **`www` → non-www** | `301` consistente a `https://datamaq.com.ar/` | — | — | OK |
| **`/courses/*` antiguas** | Cualquier URL bajo `/courses` redirige con `301` a `/cursos`, **perdiendo el slug del curso/lección**. | Media | Se pierde relevancia de la URL antigua; Google reindexa destino genérico. | Implementar redirecciones semánticas (ver mapa abajo). |
| **`/instructor/agustinbustos/`** | Devuelve `404` | Alta | Googlebot recibe 404 en una URL indexada previamente. | 301 a `/cursos/instructor/agustin-bustos`. |

**Mapa de redirecciones propuesto para Nginx (`datamaq.conf`):**

```bash
sudo cp /etc/nginx/conf.d/datamaq.conf \
        /etc/nginx/conf.d/datamaq.conf.bak-$(date +%Y%m%d-%H%M%S)
sudo nano /etc/nginx/conf.d/datamaq.conf
```

Agregar **antes** del bloque `location / { proxy_pass ... }`:

```nginx
# Redirecciones de la antigua SPA Vue a la nueva SSR
location = /courses {
    return 301 https://datamaq.com.ar/cursos;
}

# Curso antiguo -> ficha del curso nuevo (si el slug es el mismo)
location ~ ^/courses/([^/]+)/?$ {
    return 301 https://datamaq.com.ar/cursos/$1;
}

# Lección antigua -> ficha del curso nuevo (no hay equivalencia exacta de lección)
location ~ ^/courses/([^/]+)/lessons/([^/]+)/?$ {
    return 301 https://datamaq.com.ar/cursos/$1;
}

# Quiz antiguo -> ficha del curso nuevo
location ~ ^/courses/([^/]+)/quizzes/([^/]+)/?$ {
    return 301 https://datamaq.com.ar/cursos/$1;
}

# Instructor antiguo -> instructor nuevo
location ~ ^/instructor/agustinbustos/?$ {
    return 301 https://datamaq.com.ar/cursos/instructor/agustin-bustos;
}
```

> ⚠️ Es imprescindible verificar que los `slug` de curso coincidan entre la SPA antigua y la SSR nueva. Si no coinciden, conviene generar un mapa manual `map` de Nginx o redirigir todo a `/cursos` temporalmente.

Validar y recargar:

```bash
sudo nginx -t && sudo systemctl reload nginx
```

---

### 3.4 Performance / Core Web Vitals

| Métrica | Valor medido | Observación |
|---|---|---|
| **TTFB Cloudflare** | ~71–92 ms | Excelente |
| **TTFB origen directo** | ~34–43 ms | Excelente |
| **FCP / LCP / CLS / INP / TBT** | No medido | No hay `lighthouse` ni Chrome instalados. |

**Observaciones del HTML:**

- ✅ Hero image con `width="900" height="700"`, `fetchpriority="high"`, `decoding="async"`.
- ✅ Imágenes below-the-fold con `loading="lazy"` y dimensiones explícitas.
- ❌ **6 hojas de estilo externas** (`index.css`, `WhatsAppFab.css`, `useContactPageActions.css`, `HomePage.css`, `CookieBanner.css`, `LegalPage.css`) son render-blocking. No hay CSS crítico inline.
- ✅ `app.js` se carga como `type="module"` (comportamiento `defer` implícito).
- ✅ Cloudflare comprime con Brotli/Gzip.
- ✅ Estáticos cacheados 7 días con `immutable`.

**Recomendaciones de performance:**

1. Inyectar CSS crítico del above-the-fold inline en `<head>` y cargar el resto de forma asíncrona (`media="print" onload="this.media='all'"`).
2. Precargar la fuente/largest image si aplica.
3. Instalar Lighthouse para medir CWV reales:

```bash
# Ejemplo de instalación en un entorno aislado (no ejecutar sin confirmar)
npm install -g lighthouse
lighthouse https://datamaq.com.ar/ --only-categories=performance,seo,accessibility --output=html --output-path=./datamaq-lighthouse.html
```

---

### 3.5 Seguridad y Headers

| Header | Estado |
|---|---|
| `X-Frame-Options: SAMEORIGIN` | ✅ |
| `X-Content-Type-Options: nosniff` | ✅ |
| `Referrer-Policy: strict-origin-when-cross-origin` | ✅ |
| `Permissions-Policy` | ✅ |
| `Content-Security-Policy` | ❌ Ausente |
| `Strict-Transport-Security` | ❌ Ausente |

**CSP propuesta (ajustar tras probar en modo report-only):**

```nginx
add_header Content-Security-Policy
    "default-src 'self';
     script-src 'self' https://static.cloudflareinsights.com https://www.googletagmanager.com 'unsafe-inline';
     style-src 'self' https://fonts.googleapis.com 'unsafe-inline';
     font-src 'self' https://fonts.gstatic.com;
     img-src 'self' data:;
     connect-src 'self' https://www.google-analytics.com;
     frame-ancestors 'self';"
    always;
```

> Recomendación: primero desplegar en modo `Content-Security-Policy-Report-Only` para detectar violaciones sin romper nada.

---

### 3.6 Off-page

| Item | Estado |
|---|---|
| **DNS** | Resuelve a Cloudflare (`104.21.36.225`, `172.67.200.7`). |
| **IP origen** | `168.181.184.103` / `2800:6c0:5::1fbf`. |
| **rDNS** | `vps-5685053-x.dattaweb.com.` (genérico del host, no afecta SEO). |
| **Listas negras** | Chequeo básico Spamhaus no arrojó listado. |
| **robots.txt** | ✅ Permite `User-agent: *`, incluye `Sitemap: https://datamaq.com.ar/sitemap.xml`. Bloquea solo bots de IA (`GPTBot`, `ClaudeBot`, etc.), no Googlebot. |
| **Sitemap** | ✅ `https://datamaq.com.ar/sitemap.xml` devuelve `200` en `GET`. En `HEAD` da `405` por el mismo problema de HEAD. |

---

### 3.7 Logs de Nginx

**404 más frecuentes (últimos días):**

```
472 /SDK/webLanguage
337 /wp-login.php
176 /.env
152 /robots.txt
141 /favicon.ico
115 /cgi-bin/luci/;stok=/locale
103 /.git/config
```

> Son principalmente escaneos de vulnerabilidades contra la IP directa. No impactan SEO, pero saturan logs.

**5xx recientes:**

- 502 contra `n8n.datamaq.com.ar` (puerto 5678 cerrado).
- 502 contra `crm.datamaq.com.ar` (puerto 8081 cerrado).

> No afectan a `datamaq.com.ar`, pero indican servicios internos caídos.

**Googlebot en 10 días:**

```
87  200
47  301
 1  308
 7  404
```

**Ejemplos de rastreo reciente problemático:**

```text
GET /courses/bash-aplicado-a-arquitectura-y-sistemas-operativos/lessons/... 301
GET /instructor/agustinbustos/ 308 → 404
```

**Conclusión de rastreo:** Googlebot está activo, pero sigue encontrando URLs antiguas y errores 404. Se recomienda corregir redirecciones y monitorear con:

```bash
# Verificar rastreo reciente
grep -iE 'googlebot' /var/log/nginx/access.log | tail -20

# Ver errores 404 generados por crawlers
awk '$9 == 404 {print $7}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -20
```

---

## 4. Google Search Console

No es posible verificar directamente desde el servidor si el dominio está registrado en Search Console. Se recomienda:

1. Acceder a [https://search.google.com/search-console](https://search.google.com/search-console).
2. Agregar propiedad `datamaq.com.ar` (dominio o prefijo de URL).
3. Enviar el sitemap: `https://datamaq.com.ar/sitemap.xml`.
4. Revisar **Páginas** → **No indexadas** y buscar URLs afectadas por `X-Robots-Tag` o 404.
5. Usar la herramienta **Inspeccionar URL** para `/` y `/cursos` y confirmar que Google ve `index,follow`.

---

## 5. Checklist de verificación post-implementación

```bash
# 1. Backup previo
sudo cp /etc/nginx/conf.d/datamaq.conf /etc/nginx/conf.d/datamaq.conf.bak-$(date +%Y%m%d-%H%M%S)
sudo cp /etc/nginx/conf.d/security-headers-common.conf /etc/nginx/conf.d/security-headers-common.conf.bak-$(date +%Y%m%d-%H%M%S)
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak-$(date +%Y%m%d-%H%M%S)

# 2. Aplicar cambios, validar y recargar
sudo nginx -t && sudo systemctl reload nginx

# 3. Verificar redirecciones
curl -sI http://datamaq.com.ar/ | grep -E 'HTTP|Location'
curl -sI https://www.datamaq.com.ar/ | grep -E 'HTTP|Location'
curl -sI https://datamaq.com.ar/courses/arquitectura-y-sistemas-operativos/ | grep -E 'HTTP|Location'
curl -sI https://datamaq.com.ar/instructor/agustinbustos/ | grep -E 'HTTP|Location'

# 4. Verificar que HEAD ya no bloquee indexación
curl -sI https://datamaq.com.ar/ | grep -iE 'x-robots-tag|HTTP/'
curl -sI https://datamaq.com.ar/sitemap.xml | grep -iE 'x-robots-tag|HTTP/'

# 5. Verificar headers de seguridad
curl -sI https://datamaq.com.ar/ | grep -iE 'strict-transport-security|content-security-policy|x-frame-options'

# 6. Verificar compresión en edge
curl -sI -H 'Accept-Encoding: br' https://datamaq.com.ar/static/css/index.css | grep -i 'content-encoding'

# 7. Verificar CWV con Lighthouse (requiere Chrome/Lighthouse instalado)
lighthouse https://datamaq.com.ar/ --only-categories=performance,seo,accessibility

# 8. Verificar rastreo de Googlebot
grep -iE 'googlebot' /var/log/nginx/access.log | awk '{print $9}' | sort | uniq -c
```

---

## 6. Próximos pasos recomendados

1. **Corregir el comportamiento de `HEAD`** en la aplicación FastAPI para eliminar `X-Robots-Tag: noindex, nofollow`.
2. **Implementar redirecciones semánticas** `/courses/*` e `/instructor/*`.
3. **Habilitar HSTS** y evaluar CSP en modo report-only.
4. **Habilitar gzip en origen** como medida defensiva.
5. **Instalar Lighthouse/Chrome** o usar PageSpeed Insights para medir LCP, FCP, CLS, INP y TBT reales.
6. **Registrar/enviar sitemap en Google Search Console** y monitorear cobertura.
