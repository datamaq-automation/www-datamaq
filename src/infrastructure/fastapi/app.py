from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.exceptions import HTTPException
from src.infrastructure.settings import config
from src.infrastructure.fastapi.dependencies import CachedStaticFiles, templates, get_contenido
from src.infrastructure.fastapi.utils.seo import canonical_url

# --- Inicialización de FastAPI ---

app = FastAPI(title=config.APP_TITLE)
app.state.config = config
app.mount("/static", CachedStaticFiles(directory=config.STATIC_DIR), name="static")

# --- Manejadores de error ---

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        contenido = get_contenido()
        seo = {
            "title": f"P\u00e1gina no encontrada | {contenido.brand.brandName}",
            "description": "La p\u00e1gina solicitada no existe.",
            "canonical_url": canonical_url(request.url),
            "site_name": contenido.brand.brandName,
            "og_image": contenido.seo.og_image,
            "og_image_width": 1200,
            "og_image_height": 630,
        }
        context = {
            "request": request,
            "brand": contenido.brand.model_dump(),
            "content": contenido.content.model_dump(),
            "seo": seo,
            "chatwoot_token": config.CHATWOOT_TOKEN or "",
            "page_robots": "noindex,follow",
        }
        return templates.TemplateResponse(request=request, name="404.html", context=context, status_code=404)

    response = HTMLResponse(content=f"<h1>Error {exc.status_code}</h1><p>{exc.detail}</p>", status_code=exc.status_code)
    response.headers["X-Robots-Tag"] = "noindex, nofollow"
    return response

# --- Registro de Routers ---
from src.infrastructure.fastapi.routes.main_routes import router as main_router
from src.infrastructure.fastapi.routes.seo_routes import router as seo_router
from src.infrastructure.fastapi.routes.industry_routes import router as industry_router
from src.infrastructure.fastapi.routes.contact_routes import router as contact_router

# Eliminamos el prefijo para respetar la estructura de URLs solicitada
app.include_router(seo_router)
app.include_router(main_router)
app.include_router(industry_router)
app.include_router(contact_router)
