from typing import Any
from urllib.parse import urlsplit, urlunsplit


def canonical_url(request_url: Any, force_https: bool = True, strip_query: bool = True) -> str:
    """
    Build a canonical URL from a request URL.

    - Forces HTTPS if requested.
    - Strips query params if requested.
    - Keeps path and fragment as-is.
    """
    url = str(request_url)
    scheme, netloc, path, query, fragment = urlsplit(url)
    if force_https:
        scheme = "https"
    if strip_query:
        query = ""
    return urlunsplit((scheme, netloc, path, query, fragment))
