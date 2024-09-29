import json
from typing import List

from starlette.config import Config

config = Config()


class Settings:
    """Settings for the application"""

    PROJECT_NAME: str = config("PROJECT_NAME", cast=str, default="Insurance API")
    PROJECT_VERSION: str = config("PROJECT_VERSION", cast=str, default="1.0.0")

    RESOURCES_PATH: str = config("RESOURCES_PATH", cast=str, default="")
    LOG_LEVEL: str = config("LOG_LEVEL", cast=str, default="INFO").upper()
    LOG_FORMAT: str = config(
        "LOG_FORMAT",
        cast=str,
        default="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )

    LOGGER_NAME: str = config("LOGGER_NAME", cast=str, default="")

    # CORS Related configurations
    CORS_ALLOWED_ORIGINS: List[str] = json.loads(
        config("CORS_ALLOWED_ORIGINS", cast=str, default="[]")
    )
    CORS_ALLOWED_METHODS: List[str] = json.loads(
        config("CORS_ALLOWED_METHODS", cast=str, default='["*"]')
    )
    CORS_ALLOWED_HEADERS: List[str] = json.loads(
        config("CORS_ALLOWED_HEADERS", cast=str, default='["*"]')
    )

    # Database basic configuration
    INITIALIZE_DATABASE = config("INITIALIZE_DATABASE", cast=bool, default=True)
    HEALTHCHECK_DATABASE = config("HEALTHCHECK_DATABASE", cast=bool, default=False)


settings = Settings()
