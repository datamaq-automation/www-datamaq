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
    assert "Sección A: Introducción a Python y FastAPI" in response.text
    assert "Cap 1: Configuración del Entorno de Desarrollo de Python" in response.text

@pytest.mark.asyncio
async def test_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/fastapi-data-science/requisitos-tecnicos")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<h3>1.1 Requisitos técnicos</h3>" in response.text
    assert "Para seguir este curso necesitarás una computadora" in response.text
    assert "### 1.1" not in response.text

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
    assert "https://datamaq.com.ar/cursos/conversation-ai-rasa" in response.text

@pytest.mark.asyncio
async def test_rasa_course_catalog_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos")
    
    assert response.status_code == 200
    assert "Conversation AI with RASA" in response.text

@pytest.mark.asyncio
async def test_rasa_course_detail_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/conversation-ai-rasa")
    
    assert response.status_code == 200
    assert "Conversation AI with RASA" in response.text
    assert "Section A: The Rasa Framework" in response.text
    assert "Cap 1: Introduction to Chatbots and the Rasa Framework" in response.text
    assert "1.1 Technical requirements" in response.text
    assert "1.2 What is Machine Learning?" in response.text

@pytest.mark.asyncio
async def test_rasa_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/conversation-ai-rasa/technical-requirements")
    
    assert response.status_code == 200
    assert "<h3>1.1 Requisitos técnicos para Rasa</h3>" in response.text
    assert "Rasa requiere versiones específicas de Python" in response.text
    assert "### 1.1" not in response.text

