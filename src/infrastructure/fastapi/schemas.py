from typing import Dict, List
from pydantic import BaseModel

class NegocioModel(BaseModel):
    nombre: str
    titulo_pagina: str
    hero_titulo: str
    telefono: str
    whatsapp_link: str
    descripcion: str
    rango_precios: str
    cta_whatsapp: str
    cta_llamada: str
    seo_description: str
    og_image: str
    chatwoot: Dict[str, str]

class ServicioModel(BaseModel):
    nombre: str
    descripcion: str
    precio: str

class ContenidoModel(BaseModel):
    negocio: NegocioModel
    servicios: List[ServicioModel]
    faq: List[Dict[str, str]]

class IndustriaModel(BaseModel):
    industrias: Dict[str, str]
