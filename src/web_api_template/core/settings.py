import json
import os
import re
from typing import Dict, List

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
        default="%(log_color)s%(levelname)-9s%(reset)s %(asctime)s %(name)s %(message)s",
    )

    LOGGER_NAME: str = config("LOGGER_NAME", cast=str, default="")

    # CORS Related configurations
    CORS_ALLOWED_ORIGINS: list = json.loads(
        config("CORS_ALLOWED_ORIGINS", cast=str, default="[]")
    )
    CORS_ALLOWED_METHODS: list = json.loads(
        config("CORS_ALLOWED_METHODS", cast=str, default='["*"]')
    )
    CORS_ALLOWED_HEADERS: list = json.loads(
        config("CORS_ALLOWED_HEADERS", cast=str, default='["*"]')
    )

    # Database basic configuration
    INITIALIZE_DATABASE = config("INITIALIZE_DATABASE", cast=bool, default=True)
    HEALTHCHECK_DATABASE = config("HEALTHCHECK_DATABASE", cast=bool, default=False)


settings = Settings()
