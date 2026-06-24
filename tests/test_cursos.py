import pytest
from httpx import AsyncClient, ASGITransport
from src.infrastructure.fastapi.app import app

@pytest.mark.asyncio
async def test_cursos_catalog_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Catálogo de Cursos" in response.text
    assert "Construyendo Aplicaciones de Ciencia de Datos con FastAPI" in response.text

@pytest.mark.asyncio
async def test_curso_detail_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/fastapi-data-science")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Construyendo Aplicaciones de Ciencia de Datos con FastAPI" in response.text
    assert "Sección 1: Introducción a Python y FastAPI" in response.text
    assert "Cap 1: Configuración del Entorno de Desarrollo de Python" in response.text

@pytest.mark.asyncio
async def test_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/fastapi-data-science/configuracion-entorno-desarrollo")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Cap 1: Configuración del Entorno de Desarrollo de Python" in response.text
    assert "Para desarrollar aplicaciones de Ciencia de Datos eficientes con FastAPI" in response.text

@pytest.mark.asyncio
async def test_invalid_course_returns_404():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/curso-inexistente")
    
    assert response.status_code == 404
    assert "Página no encontrada" in response.text

@pytest.mark.asyncio
async def test_invalid_lesson_returns_404():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/fastapi-data-science/leccion-inexistente")
    
    assert response.status_code == 404
    assert "Página no encontrada" in response.text

@pytest.mark.asyncio
async def test_sitemap_includes_courses():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/sitemap.xml")
    
    assert response.status_code == 200
    assert "https://datamaq.com.ar/cursos" in response.text
    assert "https://datamaq.com.ar/cursos/fastapi-data-science" in response.text
