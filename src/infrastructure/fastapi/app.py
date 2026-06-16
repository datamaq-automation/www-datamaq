from fastapi import FastAPI
from src.infrastructure.settings import config
from src.infrastructure.fastapi.dependencies import CachedStaticFiles

# --- Inicialización de FastAPI ---

app = FastAPI(title=config.APP_TITLE)
app.mount("/static", CachedStaticFiles(directory=config.STATIC_DIR), name="static")

# --- Registro de Routers ---
from src.infrastructure.fastapi.routes.main_routes import router as main_router
from src.infrastructure.fastapi.routes.seo_routes import router as seo_router

# Añadimos prefijo para evitar colisiones con rutas como /dev/preview/...
app.include_router(seo_router, prefix="/seo")
app.include_router(main_router)
