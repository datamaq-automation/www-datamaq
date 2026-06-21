import os
from dotenv import load_dotenv

load_dotenv()

APP_TITLE = "Datamaq API"
STATIC_DIR = "src/infrastructure/fastapi/static"
STATIC_CACHE_SECONDS = 604800
TEMPLATES_DIR = "src/infrastructure/fastapi/templates"
CONTENT_DATA_PATH = "data/contenido.yaml"
LOGGER_NAME = "app"
CHATWOOT_TOKEN = os.getenv("CHATWOOT_WEBSITE_TOKEN")
GOOGLE_ANALYTICS_ID = os.environ.get("GOOGLE_ANALYTICS_ID", None)
CLARITY_ID = os.environ.get("CLARITY_ID", None)
ROBOTS_TXT_PATH = "src/infrastructure/fastapi/static/robots.txt"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

CHATWOOT_BASE_URL = os.getenv("CHATWOOT_BASE_URL", "https://app.chatwoot.com")
CHATWOOT_ACCOUNT_ID = os.getenv("CHATWOOT_ACCOUNT_ID")
CHATWOOT_API_TOKEN = os.getenv("CHATWOOT_API_TOKEN")