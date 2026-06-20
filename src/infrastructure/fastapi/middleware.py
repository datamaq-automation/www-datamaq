from fastapi import Request
from fastapi.responses import RedirectResponse
from urllib.parse import urlsplit, urlunsplit


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


async def canonical_redirect_middleware(request: Request, call_next):
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
        canonical = urlunsplit((scheme, host, path, "", ""))
        return RedirectResponse(url=canonical, status_code=308)

    return await call_next(request)
