import pytest
from httpx import AsyncClient, ASGITransport  # type: ignore
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_contenido, get_chatwoot_token
from src.domain.models import ContenidoModel


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
            "services": {
                "title": "Test",
                "cards": [
                    {
                        "id": "test-service",
                        "title": "Monitoreo de energía",
                        "description": "Test description",
                        "key_points": ["Punto 1"]
                    }
                ]
            },
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


app.dependency_overrides[get_contenido] = override_get_contenido
app.dependency_overrides[get_chatwoot_token] = override_get_chatwoot_token


@pytest.mark.asyncio  # type: ignore
async def test_home_has_single_h1_and_meta_tags():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    text = response.text
    assert text.count("<h1") == 1
    assert "<meta name='description'" in text
    assert "<link rel='canonical'" in text
    assert "<meta property='og:title'" in text
    assert "<meta property='og:image'" in text
    assert "<meta property='og:image:width' content='1200'" in text
    assert "<meta property='og:image:height' content='630'" in text
    assert "application/ld+json" in text
    assert "https://test/" in text  # canonical forced to https and no query params


@pytest.mark.asyncio  # type: ignore
async def test_contact_has_h1():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/contact")

    assert response.status_code == 200
    assert response.text.count("<h1") == 1
    assert "contact-hero-title" in response.text


@pytest.mark.asyncio  # type: ignore
async def test_404_has_noindex():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/pagina-que-no-existe")

    assert response.status_code == 404
    assert "noindex" in response.text


@pytest.mark.asyncio  # type: ignore
async def test_sitemap_includes_dynamic_urls():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/sitemap.xml")

    assert response.status_code == 200
    text = response.text
    assert "https://datamaq.com.ar/buenos-aires/escobar/garin.html" in text
    assert "https://datamaq.com.ar/industria/alimenticia.html" in text


@pytest.mark.asyncio  # type: ignore
async def test_localidad_canonical_is_https():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/buenos-aires/escobar/garin.html")

    assert response.status_code == 200
    assert "rel='canonical' href='https://test/buenos-aires/escobar/garin.html'" in response.text


@pytest.mark.asyncio  # type: ignore
async def test_service_cards_use_heading_tags():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    assert "c-home-service-card__title\"" in response.text
    assert "<h3" in response.text
