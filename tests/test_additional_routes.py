import pytest
from httpx import AsyncClient, ASGITransport # type: ignore
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_contenido, get_chatwoot_token
from src.domain.models import ContenidoModel

# Mock data
async def override_get_contenido():
    return ContenidoModel(
        negocio={"nombre": "Test", "titulo_pagina": "Test", "hero_titulo": "Test", "telefono": "123", "whatsapp_link": "http://test.com", "descripcion": "Test", "rango_precios": "$", "cta_whatsapp": "Test", "cta_llamada": "Test", "seo_description": "Test", "og_image": "test.jpg", "chatwoot": {"base_url": "test"}},
        servicios=[],
        faq=[]
    )

async def override_get_chatwoot_token():
    return "test_token"

app.dependency_overrides[get_contenido] = override_get_contenido
app.dependency_overrides[get_chatwoot_token] = override_get_chatwoot_token

@pytest.mark.asyncio  # type: ignore
async def test_sitemap_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/sitemap.xml")
    
    assert response.status_code == 200
    assert "application/xml" in response.headers["content-type"]
