from typing import Any
from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from urllib.parse import urlunsplit
from starlette.middleware.base import RequestResponseEndpoint


def _canonical_parts(request: Request) -> tuple[str, str, str]:
    """
    Devuelve la versión canónica (scheme, host, path) para la request.

    Reglas:
      - HTTPS cuando el reverse proxy indica HTTP (vía X-Forwarded-Proto).
      - Sin prefijo www.
      - Sin trailing slash, salvo que el path sea '/'.
    """
    scheme = request.url.scheme
    host = request.url.hostname or ""
    path = request.url.path

    # Detectar HTTPS a través del reverse proxy. Si el proxy ya redirige HTTP→HTTPS
    # y no envía este header, no forzamos redirección para evitar loops.
    forwarded_proto = request.headers.get("x-forwarded-proto")
    if forwarded_proto and forwarded_proto.lower() == "http":
        scheme = "https"

    # Normalizar www → dominio raíz
    if host.startswith("www."):
        host = host[4:]

    # Normalizar trailing slash
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")

    return scheme, host, path


async def canonical_redirect_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
    """
    Middleware que redirige con HTTP 308 a la URL canónica cuando sea necesario.

    No redirige peticiones a archivos estáticos ni a la API por motivos de trailing
    slash; sí normaliza scheme/host para todo el tráfico.
    """
    scheme, host, path = _canonical_parts(request)

    current_scheme = request.url.scheme
    current_host = request.url.hostname or ""
    current_path = request.url.path

    needs_redirect = (
        scheme != current_scheme
        or host != current_host
        or path != current_path
    )

    if needs_redirect:
        canonical = urlunsplit((scheme, host, path, request.url.query, ""))
        return RedirectResponse(url=canonical, status_code=308)

    return await call_next(request)


from src.infrastructure.settings import config

async def cache_control_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
    """
    Middleware que añade cabeceras Cache-Control a las páginas HTML y sitemaps XML.
    En desarrollo (config.DEBUG=True) o rutas de previsualización no añade caché.
    """
    response = await call_next(request)
    
    if config.DEBUG:
        return response

    path = request.url.path
    if path.startswith("/dev/preview"):
        return response

    content_type = response.headers.get("content-type", "")
    if response.status_code == 200:
        if "text/html" in content_type or "application/xml" in content_type:
            response.headers["Cache-Control"] = "public, max-age=3600, s-maxage=86400, stale-while-revalidate=60"
            
    return response
