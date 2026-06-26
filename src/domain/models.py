from typing import Dict, List, Optional, Union, Literal
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
    cta: Optional[str] = None
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
    footerDescription: str

class HeroModel(BaseModel):
    badge: str
    title: str
    cta: Optional[str] = None
    subtitle: str
    cta: Optional[str] = None
    responseNote: str
    primaryCta: CtaModel
    secondaryCta: CtaModel
    benefits: List[BenefitModel]
    image: PhotoModel

class ServiceCardModel(BaseModel):
    id: str
    title: str
    cta: Optional[str] = None
    description: str
    key_points: List[str]

class ServicesModel(BaseModel):
    title: str
    cta: Optional[str] = None
    cards: List[ServiceCardModel]

class NavbarModel(BaseModel):
    links: List[NavbarLinkModel]

class FaqModel(BaseModel):
    questions: List[FaqItemModel]

class AboutModel(BaseModel):
    title: str
    cta: Optional[str] = None
    paragraphs: List[str]
    image: PhotoModel

class ProfileModel(BaseModel):
    bullets: List[str]

class LegalModel(BaseModel):
    text: str

class CookieBannerModel(BaseModel):
    title: str
    text: str
    accept_label: str
    reject_label: str
    more_info_label: str
    more_info_link: str

class LegalSectionModel(BaseModel):
    title: str
    paragraphs: List[str]

class LegalPageModel(BaseModel):
    title: str
    last_updated: str
    introduction: str
    sections: List[LegalSectionModel]

class LegalPagesModel(BaseModel):
    terms: LegalPageModel

# --- Nuevos Modelos Contact ---
class FieldModel(BaseModel):
    id: str
    label: str
    autocomplete: Optional[str] = None

class StepModel(BaseModel):
    title: str
    cta: Optional[str] = None
    fields: List[FieldModel]

class AltEmailModel(BaseModel):
    label: str
    title: str
    cta: Optional[str] = None
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
    cta: Optional[str] = None
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
    cookie_banner: CookieBannerModel

class FooterLinkModel(BaseModel):
    label: str
    href: str

class FooterGroupModel(BaseModel):
    title: str
    links: List[FooterLinkModel]

class FooterModel(BaseModel):
    navigation_groups: List[FooterGroupModel]
    cta_title: str
    cta_label: str
    whatsapp_text: str
    terms_label: str
    terms_href: str
    copyright_suffix: str

class ContenidoModel(BaseModel):
    brand: BrandModel
    content: ContentModel
    seo: SeoModel
    legal_pages: LegalPagesModel
    footer: FooterModel

class IndustriaModel(BaseModel):
    industrias: Dict[str, str]

# --- Modelos de Cursos (LMS) ---
class InstructorSocialLinksModel(BaseModel):
    linkedin: Optional[str] = None
    github: Optional[str] = None
    twitter: Optional[str] = None
    website: Optional[str] = None

class InstructorModel(BaseModel):
    id: str
    name: str
    role: str
    photo: str
    bio: str
    social_links: Optional[InstructorSocialLinksModel] = None

class InstructoresContainerModel(BaseModel):
    instructores: List[InstructorModel]

class LessonModel(BaseModel):
    type: Literal["lesson"] = "lesson"
    id: str
    slug: str
    title: str
    duration: str
    content_type: str  # "markdown" | "video"
    video_url: Optional[str] = None
    content: Optional[str] = None
    content_file: Optional[str] = None

class QuestionModel(BaseModel):
    id: str
    question: str
    type: str  # "single_choice" | "true_false"
    options: List[str]
    correct_option: int  # Índice de la opción correcta (0-indexed)
    explanation: Optional[str] = None

class QuizModel(BaseModel):
    type: Literal["quiz"] = "quiz"
    id: str
    slug: str
    title: str
    duration: str
    questions: List[QuestionModel]

class CourseChapterModel(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    items: List[Union[LessonModel, QuizModel]]

class CourseSectionModel(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    chapters: List[CourseChapterModel]

class CourseModel(BaseModel):
    id: str
    slug: str
    title: str
    description_short: str
    description_long: str
    duration: str
    level: str
    language: str
    price: float
    og_image: Optional[str] = None
    instructor: InstructorModel
    sections: List[CourseSectionModel]

class CursosContainerModel(BaseModel):
    cursos: List[CourseModel]

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
