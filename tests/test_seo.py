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
def setup_dependency_overrides():
    app.dependency_overrides[get_contenido] = override_get_contenido
    app.dependency_overrides[get_chatwoot_token] = override_get_chatwoot_token
    yield
    app.dependency_overrides.clear()


async def override_get_chatwoot_token():
    return "test_token"


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
    assert "https://datamaq.com.ar/" in text  # canonical forced to production base URL and no query params


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
        response_unknown = await ac.get("/pagina-que-no-existe")
        response_business = await ac.get("/cursos/curso-que-no-existe")

    assert response_unknown.status_code == 301
    assert response_unknown.headers["location"] == "/"
    
    assert response_business.status_code == 404
    assert "noindex" in response_business.text


@pytest.mark.asyncio  # type: ignore
async def test_sitemap_includes_dynamic_urls():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/sitemap.xml")

    assert response.status_code == 200
    text = response.text
    assert "https://datamaq.com.ar/buenos-aires/escobar/garin.html" in text
    assert "https://datamaq.com.ar/industria/grafica.html" in text


@pytest.mark.asyncio  # type: ignore
async def test_localidad_canonical_is_https():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/buenos-aires/escobar/garin.html")

    assert response.status_code == 200
    assert "rel='canonical' href='https://datamaq.com.ar/buenos-aires/escobar/garin.html'" in response.text


@pytest.mark.asyncio  # type: ignore
async def test_service_cards_use_heading_tags():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    assert "c-home-service-card__title\"" in response.text
    assert "<h3" in response.text


import re
import json

def parse_json_ld_blocks(html: str) -> list:
    """
    Busca todos los bloques <script type="application/ld+json"> en el HTML
    y los carga como objetos JSON. Levanta AssertionError en caso de sintaxis inválida.
    """
    pattern = re.compile(r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>', re.DOTALL)
    blocks = pattern.findall(html)
    parsed = []
    for b in blocks:
        try:
            parsed.append(json.loads(b.strip()))
        except json.JSONDecodeError as e:
            pytest.fail(f"Sintaxis JSON-LD corrupta o inválida: {b}\nError: {e}")
    return parsed

def get_json_ld_by_type(json_ld_list, target_type):
    """
    Busca en una lista de diccionarios de JSON-LD el tipo especificado,
    manejando tanto estructuras planas como anidadas bajo @graph.
    """
    for item in json_ld_list:
        if isinstance(item, dict):
            if "@graph" in item:
                for sub_item in item["@graph"]:
                    if isinstance(sub_item, dict) and sub_item.get("@type") == target_type:
                        return sub_item
            elif item.get("@type") == target_type:
                return item
    return None

@pytest.mark.asyncio  # type: ignore
async def test_json_ld_syntax_and_schemas():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Validar Home (Organization, WebPage, FAQPage)
        response_home = await ac.get("/")
        assert response_home.status_code == 200
        json_lds_home = parse_json_ld_blocks(response_home.text)
        assert len(json_lds_home) > 0, "No se encontraron bloques JSON-LD en la Home"
        
        org = get_json_ld_by_type(json_lds_home, "Organization")
        webpage = get_json_ld_by_type(json_lds_home, "WebPage")
        faq = get_json_ld_by_type(json_lds_home, "FAQPage")
        
        assert org is not None, "Falta JSON-LD de tipo Organization en la Home"
        assert webpage is not None, "Falta JSON-LD de tipo WebPage en la Home"
        assert faq is not None, "Falta JSON-LD de tipo FAQPage en la Home"
        
        assert org.get("name") is not None
        assert webpage.get("name") is not None
        assert faq.get("mainEntity") is not None

        # 2. Validar Localidad (LocalBusiness)
        response_loc = await ac.get("/buenos-aires/escobar/garin.html")
        assert response_loc.status_code == 200
        json_lds_loc = parse_json_ld_blocks(response_loc.text)
        local_business = get_json_ld_by_type(json_lds_loc, "LocalBusiness")
        assert local_business is not None, "Falta JSON-LD de tipo LocalBusiness en la página de localidad"
        assert local_business.get("address") is not None
        assert local_business["address"].get("addressLocality") == "Garín"
        assert local_business.get("areaServed") is not None

        # 3. Validar Industria (Service)
        response_ind = await ac.get("/industria/grafica.html")
        assert response_ind.status_code == 200
        json_lds_ind = parse_json_ld_blocks(response_ind.text)
        service = get_json_ld_by_type(json_lds_ind, "Service")
        assert service is not None, "Falta JSON-LD de tipo Service en la página de industria"
        assert "Industria Gráfica" in service.get("name", "")
        assert service.get("provider") is not None

@pytest.mark.asyncio  # type: ignore
async def test_json_ld_cursos_and_breadcrumbs():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Validar Detalle del Curso (Course, BreadcrumbList)
        response_detail = await ac.get("/cursos/fastapi-data-science")
        assert response_detail.status_code == 200
        json_lds_detail = parse_json_ld_blocks(response_detail.text)
        
        course = get_json_ld_by_type(json_lds_detail, "Course")
        breadcrumbs_detail = get_json_ld_by_type(json_lds_detail, "BreadcrumbList")
        
        assert course is not None, "Falta JSON-LD de tipo Course en el detalle del curso"
        assert breadcrumbs_detail is not None, "Falta JSON-LD de tipo BreadcrumbList en el detalle del curso"
        assert "FastAPI" in course.get("name", "")
        assert len(breadcrumbs_detail.get("itemListElement", [])) == 3

        # 2. Validar Lección (BreadcrumbList)
        response_lesson = await ac.get("/cursos/fastapi-data-science/requisitos-tecnicos")
        assert response_lesson.status_code == 200
        json_lds_lesson = parse_json_ld_blocks(response_lesson.text)
        
        breadcrumbs_lesson = get_json_ld_by_type(json_lds_lesson, "BreadcrumbList")
        assert breadcrumbs_lesson is not None, "Falta JSON-LD de tipo BreadcrumbList en la página de lección"
        assert len(breadcrumbs_lesson.get("itemListElement", [])) == 3
        # Comprobar que el tercer elemento es la lección actual
        assert "Requisitos técnicos" in breadcrumbs_lesson["itemListElement"][2]["name"]
