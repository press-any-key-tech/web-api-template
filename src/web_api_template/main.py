from fastapi import FastAPI

from web_api_template.application import start_application
from web_api_template.core.settings import settings

app: FastAPI = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)
start_application(app)
