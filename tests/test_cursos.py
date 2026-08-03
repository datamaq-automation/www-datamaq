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
    assert "Cursos y capacitaciones técnicas gratuitas" in response.text
    assert "Desarrollo de APIs con FastAPI y Python" in response.text
    assert "FastAPI Avanzado: MLOps, Async DB y Producción" in response.text

@pytest.mark.asyncio
async def test_curso_detail_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/fastapi-intermedio")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Desarrollo de APIs con FastAPI y Python" in response.text
    assert "Sección A: Fundamentos de Python y Entorno" in response.text
    assert "Cap 1: Entorno de Desarrollo de Python" in response.text

@pytest.mark.asyncio
async def test_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/fastapi-intermedio/instalacion-distribucion-python-pyenv")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "1.1 Instalación de una Distribución de Python con pyenv" in response.text
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
        response = await ac.get("/cursos/fastapi-intermedio/leccion-inexistente")
    
    assert response.status_code == 404
    assert "Página no encontrada" in response.text

@pytest.mark.asyncio
async def test_sitemap_includes_courses():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/sitemap.xml")
    
    assert response.status_code == 200
    assert "https://datamaq.com.ar/cursos" in response.text
    assert "https://datamaq.com.ar/cursos/fastapi-intermedio" in response.text
    assert "https://datamaq.com.ar/cursos/fastapi-avanzado" in response.text


@pytest.mark.asyncio
async def test_default_instructor_redirects():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/instructor", follow_redirects=False)
    
    assert response.status_code == 307
    assert response.headers["location"] == "/cursos/instructor/agustin-bustos"


@pytest.mark.asyncio
async def test_instructor_detail_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/instructor/agustin-bustos")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Agustin Bustos" in response.text
    assert "Mantenimiento Industrial" in response.text
    assert "Desarrollo de APIs con FastAPI y Python" in response.text


@pytest.mark.asyncio
async def test_invalid_instructor_returns_404():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/instructor/inexistente")
    
    assert response.status_code == 404
    assert "Página no encontrada" in response.text


@pytest.mark.asyncio
async def test_energia_course_catalog_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos")
    
    assert response.status_code == 200
    assert "Instalaciones y Aplicaciones de la Energía" in response.text


@pytest.mark.asyncio
async def test_energia_course_detail_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/instalaciones-aplicaciones-energia")
    
    assert response.status_code == 200
    assert "Instalaciones y Aplicaciones de la Energía" in response.text
    assert "Sección A: Media Tensión y Conversión de Energía" in response.text
    assert "Líneas de Distribución en 13.2 kV" in response.text


@pytest.mark.asyncio
async def test_energia_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/instalaciones-aplicaciones-energia/lineas-13-2kv")
    
    assert response.status_code == 200
    assert "Características y tipos de líneas de 13.2 kV" in response.text
    assert "Conductores Desnudos" in response.text


@pytest.mark.asyncio
async def test_energia_new_lessons_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Puesta a Tierra
        response = await ac.get("/cursos/instalaciones-aplicaciones-energia/puesta-a-tierra")
        assert response.status_code == 200
        assert "Diseño de Puesta a Tierra y Seguridad Eléctrica" in response.text
        assert "Tensión de Contacto" in response.text

        # Coordinación y Selectividad
        response = await ac.get("/cursos/instalaciones-aplicaciones-energia/coordinacion-selectividad")
        assert response.status_code == 200
        assert "Coordinación de Protecciones y Selectividad" in response.text
        assert "ANSI 50" in response.text

        # Ensayos y Mantenimiento
        response = await ac.get("/cursos/instalaciones-aplicaciones-energia/ensayos-mantenimiento")
        assert response.status_code == 200
        assert "Ensayos de Campo y Mantenimiento Predictivo" in response.text
        assert "DGA" in response.text

        # Calidad de Energía
        response = await ac.get("/cursos/instalaciones-aplicaciones-energia/calidad-energia")
        assert response.status_code == 200
        assert "Calidad de Energía y Compensación de Reactiva" in response.text
        assert "THD-I" in response.text

        # Sistemas de Gestión de Energía
        response = await ac.get("/cursos/instalaciones-aplicaciones-energia/sistemas-gestion-energia-iot")
        assert response.status_code == 200
        assert "Sistemas de Gestión de Energía (SGE) e IoT" in response.text
        assert "Modbus" in response.text

        # Generación Distribuida
        response = await ac.get("/cursos/instalaciones-aplicaciones-energia/generacion-distribuida")
        assert response.status_code == 200
        assert "Transición Energética y Generación Distribuida" in response.text
        assert "BESS" in response.text


@pytest.mark.asyncio
async def test_curso_detail_includes_image_dimensions():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/fastapi-intermedio")
    assert response.status_code == 200
    assert 'width="1200"' in response.text
    assert 'height="630"' in response.text


@pytest.mark.asyncio
async def test_cursos_pages_do_not_render_footer():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        for url in [
            "/cursos",
            "/cursos/fastapi-intermedio",
            "/cursos/fastapi-intermedio/instalacion-distribucion-python-pyenv",
            "/cursos/instructor/agustin-bustos",
        ]:
            response = await ac.get(url)
            assert response.status_code == 200
            assert 'class="c-home-footer"' not in response.text

