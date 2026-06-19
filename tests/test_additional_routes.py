import pytest
from httpx import AsyncClient, ASGITransport # type: ignore
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_contenido, get_chatwoot_token
from src.domain.models import ContenidoModel

# Mock data actualizado a la nueva estructura
async def override_get_contenido():
    return ContenidoModel(
        brand={
            "brandName": "Test",
            "brandAriaLabel": "Test",
            "baseOperativa": "Test",
            "contactEmail": "test@test.com",
            "whatsappUrl": "http://test.com",
            "technician": {"name": "Test", "role": "Test", "photo": {"src": "test.jpg", "alt": "Test"}}
        },
        content={
            "hero": {
                "badge": "Test", "title": "Test", "subtitle": "Test", "responseNote": "Test",
                "primaryCta": {"label": "Test", "href": "http://test.com"},
                "secondaryCta": {"label": "Test", "href": "http://test.com"},
                "benefits": [],
                "image": {"src": "test.jpg", "alt": "Test"}
            },
            "services": {"title": "Test", "cards": []},
            "navbar": {"links": []},
            "faq": {"questions": []},
            "about": {"title": "Test", "paragraphs": [], "image": {"src": "test.jpg", "alt": "Test"}},
            "profile": {"bullets": []},
            "legal": {"text": "Test"},
            "cookie_banner": {
                "title": "Test",
                "text": "Test",
                "accept_label": "Aceptar",
                "reject_label": "Rechazar",
                "more_info_label": "Ver m\u00e1s",
                "more_info_link": "/terminos-y-condiciones"
            },
            "contact": {
                "title": "Test",
                "subtitle": "Test",
                "cta": "Test",
                "alt_email": {"label": "Test", "title": "Test", "email": "test@test.com"},
                "progress_text": "Test",
                "privacy_note": "Test",
                "error_message": "Test",
                "optional_text": "Test",
                "steps": []
            }
        },
        seo={"title": "Test", "description": "Test", "site_name": "Test", "canonical_url": "http://test.com", "og_image": "http://test.com/og.png"},
        legal_pages={
            "terms": {
                "title": "T\u00e9rminos y condiciones",
                "last_updated": "2026-06-19",
                "introduction": "Test",
                "sections": [{"title": "Test", "paragraphs": ["Test"]}]
            }
        }
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

@pytest.mark.asyncio  # type: ignore
async def test_terms_page_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/terminos-y-condiciones")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "T\u00e9rminos y condiciones" in response.text

@pytest.mark.asyncio  # type: ignore
async def test_contact_page_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/contact")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Consultor\u00eda t\u00e9cnica IoT" in response.text

@pytest.mark.asyncio  # type: ignore
async def test_custom_404_page_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/pagina-que-no-existe")
    
    assert response.status_code == 404
    assert "text/html" in response.headers["content-type"]
    assert "P\u00e1gina no encontrada" in response.text

@pytest.mark.asyncio  # type: ignore
async def test_sitemap_includes_contact():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/sitemap.xml")
    
    assert response.status_code == 200
    assert "https://datamaq.com.ar/contact" in response.text

@pytest.mark.asyncio  # type: ignore
async def test_localidad_page_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/buenos-aires/escobar/garin.html")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Gar\u00edn" in response.text
    assert "Captura de datos operativos" in response.text

@pytest.mark.asyncio  # type: ignore
async def test_industria_page_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/industria/alimenticia.html")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Industria Alimenticia" in response.text
    assert "Captura de datos" in response.text
