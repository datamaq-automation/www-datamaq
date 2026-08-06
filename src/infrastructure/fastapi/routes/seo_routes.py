from typing import Any, Dict
from fastapi import APIRouter, Request, HTTPException, Depends
from src.infrastructure.fastapi.dependencies import templates, get_contenido, get_geografia, get_landing_content
from src.infrastructure.fastapi.utils.seo import canonical_url
from src.domain.models import ContenidoModel, LandingContentModel
from src.adapters.presenters.content_presenter import present_contenido

router = APIRouter()

@router.get("/{provincia}")
async def pagina_provincia(
    request: Request,
    provincia: str,
    contenido: ContenidoModel = Depends(get_contenido),
    geografia: Dict[str, Any] = Depends(get_geografia),
):
    """Página hub de provincia: lista los municipios y sus localidades."""
    locs: Dict[str, Any] = geografia.get("localidades", {})
    prov = locs.get(provincia)

    if not prov:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")

    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    provincia_nombre = provincia.replace("-", " ").title()

    # Armar lista de municipios con sus localidades
    municipios_list = []
    all_localidades: list[dict] = []
    for muni_key, localidades in prov.items():
        muni_nombre = muni_key.replace("-", " ").title()
        loc_list = []
        for loc_key, loc_nombre in localidades.items():
            loc_url = f"/{provincia}/{muni_key}/{loc_key}.html"
            loc_list.append({"nombre": loc_nombre, "url": loc_url})
            all_localidades.append({"nombre": loc_nombre, "url": loc_url, "municipio": muni_nombre})
        muni_url = f"/{provincia}/{muni_key}"
        municipios_list.append({"nombre": muni_nombre, "slug": muni_key, "localidades": loc_list})

    seo = {
        "title": f"Asistencia técnica en {provincia_nombre} | DataMaq",
        "description": f"Servicios de mantenimiento eléctrico industrial, monitoreo de energía e IoT en {provincia_nombre}. Visitas en campo y consultoría remota para Oil & Gas e industria.",
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: Dict[str, Any] = {
        "brand": brand_data,
        "content": presented["content"],
        "seo": seo,
        "footer": presented.get("footer"),
        "hub_type": "provincia",
        "hub_title": f"Asistencia técnica en {provincia_nombre}",
        "hub_subtitle": f"Seleccioná tu municipio para ver la cobertura en {provincia_nombre}.",
        "municipios": municipios_list,
        "provincia": provincia_nombre,
        "provincia_slug": provincia,
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)


@router.get("/{provincia}/{municipio}")
async def pagina_municipio(
    request: Request,
    provincia: str,
    municipio: str,
    contenido: ContenidoModel = Depends(get_contenido),
    geografia: Dict[str, Any] = Depends(get_geografia),
):
    """Página hub de municipio: lista las localidades."""
    locs: Dict[str, Any] = geografia.get("localidades", {})
    prov = locs.get(provincia)

    if not prov:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")

    mun = prov.get(municipio)
    if not mun:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")

    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    provincia_nombre = provincia.replace("-", " ").title()
    municipio_nombre = municipio.replace("-", " ").title()

    localidades_list = []
    for loc_key, loc_nombre in mun.items():
        localidades_list.append({
            "nombre": loc_nombre,
            "url": f"/{provincia}/{municipio}/{loc_key}.html",
        })

    seo = {
        "title": f"Asistencia técnica en {municipio_nombre}, {provincia_nombre} | DataMaq",
        "description": f"Servicios de mantenimiento eléctrico industrial, monitoreo de energía e IoT en {municipio_nombre}, {provincia_nombre}. Visitas en campo y consultoría remota.",
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: Dict[str, Any] = {
        "brand": brand_data,
        "content": presented["content"],
        "seo": seo,
        "footer": presented.get("footer"),
        "hub_type": "municipio",
        "hub_title": f"Asistencia técnica en {municipio_nombre}",
        "hub_subtitle": f"Seleccioná tu localidad en {municipio_nombre}, {provincia_nombre} para ver la cobertura.",
        "localidades": localidades_list,
        "municipio": municipio_nombre,
        "municipio_slug": municipio,
        "provincia": provincia_nombre,
        "provincia_slug": provincia,
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)


@router.get("/{provincia}/{municipio}/{localidad}.html")
async def pagina_localidad(request: Request, provincia: str, municipio: str, localidad: str, contenido: ContenidoModel = Depends(get_contenido), geografia: Dict[str, Any] = Depends(get_geografia), landing_content: LandingContentModel = Depends(get_landing_content)):
    # Validar existencia
    locs: Dict[str, Any] = geografia.get("localidades", {})
    prov = locs.get(provincia, {})
    mun = prov.get(municipio, {})
    nombre_localidad = mun.get(localidad)

    if not nombre_localidad:
        raise HTTPException(status_code=404, detail="Localidad no encontrada")

    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]
    servicios_data = content_data["services"]["cards"]
    
    municipio_formateado = municipio.replace("-", " ").title()

    localidad_content = (
        landing_content.localidades
        .get(provincia, {})
        .get(municipio, {})
        .get(localidad)
    )

    seo = {
        "title": f"Asistencia técnica en {nombre_localidad}, {municipio_formateado} | DataMaq",
        "description": f"Visitas técnicas en campo y asistencia remota para monitoreo de energía industrial e IoT en {nombre_localidad}. Capacitaciones de cortesía según el proyecto.",
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    hero_title = f"Asistencia técnica en {nombre_localidad}"
    hero_subtitle = f"Visitas en campo y consultoría remota para monitoreo de energía, captura de datos operativos e IoT industrial en {nombre_localidad}, {municipio_formateado}."

    context: Dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "servicios": servicios_data,
        "faq": content_data["faq"]["questions"],
        "localidad_nombre": nombre_localidad,
        "municipio": municipio_formateado,
        "provincia": provincia.replace("-", " ").title(),
        "seo": seo,
        "footer": presented.get("footer"),
        "hero_title": hero_title,
        "hero_subtitle": hero_subtitle,
        "landing_localidad": localidad_content.model_dump() if localidad_content else None,
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)
