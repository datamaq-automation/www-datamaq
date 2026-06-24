import pytest
import tempfile
from unittest.mock import patch
from httpx import AsyncClient, ASGITransport # type: ignore
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_contenido, get_chatwoot_token, get_chatwoot_gateway
from src.domain.models import ContenidoModel
from src.infrastructure.gateways.chatwoot_gateway_stub import ChatwootGatewayStub

# Mock data actualizado a la nueva estructura
# Mock data actualizado a la nueva estructura
async def override_get_contenido():
    return ContenidoModel(
        brand={
            "brandName": "Test",
            "brandAriaLabel": "Test",
            "baseOperativa": "Test",
            "contactEmail": "test@test.com",
            "whatsappUrl": "http://test.com",
            "technician": {"name": "Test", "role": "Test", "photo": {"src": "test.jpg", "alt": "Test"}},
            "footerDescription": "Test footer description"
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
                "more_info_label": "Ver más",
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
                "title": "Términos y condiciones",
                "last_updated": "2026-06-19",
                "introduction": "Test",
                "sections": [{"title": "Test", "paragraphs": ["Test"]}]
            }
        },
        footer={
            "navigation_groups": [
                {
                    "title": "Navegación",
                    "links": [
                        {"label": "Inicio", "href": "/"},
                        {"label": "Cursos", "href": "/cursos"},
                        {"label": "Contacto", "href": "/contact"}
                    ]
                }
            ],
            "cta_title": "Test CTA Title",
            "cta_label": "Test CTA Label",
            "whatsapp_text": "Test WhatsApp text",
            "terms_label": "Test Terms Label",
            "terms_href": "/terminos-y-condiciones",
            "copyright_suffix": "Test copyright suffix"
        }
    )

@pytest.fixture(autouse=True)
def clean_dependency_overrides():
    yield
    app.dependency_overrides.clear()

async def override_get_chatwoot_token():
    return "test_token"

async def override_get_chatwoot_gateway():
    return ChatwootGatewayStub()

app.dependency_overrides[get_contenido] = override_get_contenido
app.dependency_overrides[get_chatwoot_token] = override_get_chatwoot_token
app.dependency_overrides[get_chatwoot_gateway] = override_get_chatwoot_gateway

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
    assert "Términos y condiciones" in response.text

@pytest.mark.asyncio  # type: ignore
async def test_contact_page_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/contact")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Consultoría técnica IoT" in response.text

@pytest.mark.asyncio  # type: ignore
async def test_custom_404_page_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/pagina-que-no-existe")
    
    assert response.status_code == 404
    assert "text/html" in response.headers["content-type"]
    assert "Página no encontrada" in response.text

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
    assert "Garín" in response.text
    assert "Captura de datos operativos" in response.text

@pytest.mark.asyncio  # type: ignore
async def test_industria_page_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/industria/grafica.html")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Industria Alimenticia" in response.text
    assert "Captura de datos" in response.text


@pytest.mark.asyncio  # type: ignore
async def test_submit_contact_returns_success():
    transport = ASGITransport(app=app)
    payload = {
        "name": "Test User",
        "comment": "Test comment",
        "email": "test@example.com",
        "createdAt": "2026-06-20T00:00:00Z",
        "pageLocation": "http://test/contact"
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch("src.infrastructure.persistence.json.lead_repository_json.DATA_DIR", tmpdir):
            async with AsyncClient(transport=transport, base_url="http://test") as ac:
                response = await ac.post("/api/v1/contact", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["submitStatus"] == "success"
    assert "requestId" in data
    assert "submissionId" in data
    assert data["submissionId"].startswith("lead_")


@pytest.mark.asyncio  # type: ignore
async def test_submit_contact_returns_partial_success_when_chatwoot_fails():
    transport = ASGITransport(app=app)
    payload = {
        "name": "Test User",
        "comment": "Test comment",
        "email": "test@example.com",
        "createdAt": "2026-06-20T00:00:00Z",
        "pageLocation": "http://test/contact"
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch("src.infrastructure.persistence.json.lead_repository_json.DATA_DIR", tmpdir):
            with patch("src.infrastructure.gateways.chatwoot_gateway_stub.ChatwootGatewayStub.create_contact", side_effect=Exception("Chatwoot down")):
                async with AsyncClient(transport=transport, base_url="http://test") as ac:
                    response = await ac.post("/api/v1/contact", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["submitStatus"] == "partial_success"
    assert "requestId" in data
    assert "submissionId" in data
    assert data["submissionId"].startswith("lead_")
