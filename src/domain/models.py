from typing import Dict, List, Optional
from pydantic import BaseModel

# --- Modelos Base ---
class PhotoModel(BaseModel):
    src: str
    alt: str

class TechnicianModel(BaseModel):
    name: str
    role: str
    photo: str

class CtaModel(BaseModel):
    label: str
    href: str

class BenefitModel(BaseModel):
    title: str
    text: str

class NavbarLinkModel(BaseModel):
    label: str
    href: str

class FaqItemModel(BaseModel):
    question: str
    answer: str

# --- Modelos de Componentes ---
class BrandModel(BaseModel):
    brandName: str
    brandAriaLabel: str
    baseOperativa: str
    contactEmail: str
    whatsappUrl: str
    technician: Optional[TechnicianModel] = None

class HeroModel(BaseModel):
    badge: str
    title: str
    subtitle: str
    responseNote: str
    primaryCta: CtaModel
    secondaryCta: CtaModel
    benefits: List[BenefitModel]
    image: PhotoModel

class ServiceCardModel(BaseModel):
    id: str
    title: str
    description: str
    key_points: List[str]

class ServicesModel(BaseModel):
    title: str
    cards: List[ServiceCardModel]

class NavbarModel(BaseModel):
    links: List[NavbarLinkModel]

class FaqModel(BaseModel):
    questions: List[FaqItemModel]

class AboutModel(BaseModel):
    title: str
    paragraphs: List[str]

class ProfileModel(BaseModel):
    bullets: List[str]

class SeoModel(BaseModel):
    siteDescription: str
    siteName: str
    siteUrl: str

# --- Modelos Principales (Deben ir después de sus componentes) ---
class ContentModel(BaseModel):
    hero: HeroModel
    services: ServicesModel
    navbar: NavbarModel
    faq: FaqModel
    about: AboutModel
    profile: ProfileModel

class ContenidoModel(BaseModel):
    brand: BrandModel
    content: ContentModel
    seo: SeoModel

class IndustriaModel(BaseModel):
    industrias: Dict[str, str]
