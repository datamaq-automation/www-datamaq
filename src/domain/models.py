from typing import Dict, List, Optional
from pydantic import BaseModel

class PhotoModel(BaseModel):
    src: str
    alt: str

class TechnicianModel(BaseModel):
    name: str
    role: str
    photo: str

class BrandModel(BaseModel):
    brandName: str
    brandAriaLabel: str
    baseOperativa: str
    contactEmail: str
    whatsappUrl: str
    technician: Optional[TechnicianModel] = None

class CtaModel(BaseModel):
    label: str
    href: str

class BenefitModel(BaseModel):
    title: str
    text: str

class HeroModel(BaseModel):
    badge: str
    title: str
    subtitle: str
    image: PhotoModel
    responseNote: str
    primaryCta: CtaModel
    secondaryCta: CtaModel
    benefits: List[BenefitModel]

class ServiceCardModel(BaseModel):
    id: str
    title: str
    description: str
    key_points: List[str]

class ServicesModel(BaseModel):
    title: str
    cards: List[ServiceCardModel]

class NavbarLinkModel(BaseModel):
    label: str
    href: str

class NavbarModel(BaseModel):
    links: List[NavbarLinkModel]

class FaqItemModel(BaseModel):
    question: str
    answer: str

class FaqModel(BaseModel):
    questions: List[FaqItemModel]

class SeoModel(BaseModel):
    siteDescription: str
    siteName: str
    siteUrl: str

class ContentModel(BaseModel):
    hero: HeroModel
    services: ServicesModel
    navbar: NavbarModel
    faq: FaqModel

class ContenidoModel(BaseModel):
    brand: BrandModel
    content: ContentModel
    seo: SeoModel

class IndustriaModel(BaseModel):
    industrias: Dict[str, str]

class ContactSubmitPayload(BaseModel):
    name: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    geographicLocation: Optional[str] = None
    comment: str
    preferredContactChannel: Optional[str] = "whatsapp"
    pageLocation: Optional[str] = None
    trafficSource: Optional[str] = None
    userAgent: Optional[str] = None
    createdAt: str
    captchaToken: Optional[str] = None
