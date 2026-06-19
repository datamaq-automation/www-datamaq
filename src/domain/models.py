from typing import Dict, List, Optional
from pydantic import BaseModel

# --- Modelos Base ---
class PhotoModel(BaseModel):
    src: str
    alt: str
    width: Optional[int] = None
    height: Optional[int] = None

class TechnicianModel(BaseModel):
    name: str
    role: str
    photo: PhotoModel

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
    technician: TechnicianModel

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
    image: PhotoModel

class ProfileModel(BaseModel):
    bullets: List[str]

class LegalModel(BaseModel):
    text: str

# --- Nuevos Modelos Contact ---
class FieldModel(BaseModel):
    id: str
    label: str
    autocomplete: str

class StepModel(BaseModel):
    title: str
    fields: List[FieldModel]

class AltEmailModel(BaseModel):
    label: str
    title: str
    email: str

class ContactModel(BaseModel):
    title: str
    subtitle: str
    cta: str
    alt_email: AltEmailModel
    progress_text: str
    privacy_note: str
    error_message: str
    optional_text: str
    steps: List[StepModel]

# --- Campos obligatorios para Fail-Fast ---
class SeoModel(BaseModel):
    title: str
    description: str
    canonical_url: str
    site_name: str
    og_image: str

# --- Modelos Principales ---
class ContentModel(BaseModel):
    hero: HeroModel
    services: ServicesModel
    navbar: NavbarModel
    faq: FaqModel
    about: AboutModel
    profile: ProfileModel
    legal: LegalModel
    contact: ContactModel

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
