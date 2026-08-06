import os
from dotenv import load_dotenv

load_dotenv()

APP_TITLE = "Datamaq API"
STATIC_DIR = "static"
STATIC_CACHE_SECONDS = 604800
TEMPLATES_DIR = "templates"
CONTENT_DATA_PATH = "data/contenido.yaml"
LOGGER_NAME = "app"
GOOGLE_ANALYTICS_ID = os.environ.get("GOOGLE_ANALYTICS_ID", None)
GOOGLE_ADS_ID = os.environ.get("GOOGLE_ADS_ID", None)
GOOGLE_ADS_CONVERSION_ID = os.environ.get("GOOGLE_ADS_CONVERSION_ID", None)
GOOGLE_ADS_WHATSAPP_CONVERSION_ID = os.environ.get("GOOGLE_ADS_WHATSAPP_CONVERSION_ID", None)
CLARITY_ID = os.environ.get("CLARITY_ID", None)
ROBOTS_TXT_PATH = "static/robots.txt"
HUMANS_TXT_PATH = "static/humans.txt"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# SMTP para notificaciones de leads por email
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL", "")

WHATSAPP_PHONE = os.getenv("WHATSAPP_PHONE", "541156297160")
WHATSAPP_MESSAGE = os.getenv("WHATSAPP_MESSAGE", "Hola! Vi tu sitio datamaq.com.ar y quería consultarte sobre servicios de mantenimiento eléctrico industrial.")

BASE_URL = os.getenv("BASE_URL", "https://datamaq.com.ar")