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
    SQLALCHEMY_DATABASE_URI = config(
        "SQLALCHEMY_DATABASE_URI",
        cast=str,
        default=None,
    )

    # Database fine tunning parameters
    POOL_SIZE = config("POOL_SIZE", cast=int, default=5)
    MAX_OVERFLOW = config("MAX_OVERFLOW", cast=int, default=-1)
    POOL_PRE_PING = config("POOL_PRE_PING", cast=bool, default=True)
    ECHO = config("ECHO", cast=bool, default=False)
    POOL_RECYCLE_IN_SECONDS = config("POOL_RECYCLE_IN_SECONDS", cast=int, default=3600)
    ECHO_POOL = config("ECHO_POOL", cast=bool, default=False)
    POOL_RESET_ON_RETURN = config("POOL_RESET_ON_RETURN", cast=str, default="rollback")
    POOL_TIMEOUT_IN_SECONDS = config("POOL_TIMEOUT_IN_SECONDS", cast=int, default=30)
    POOL = config("POOL", cast=str, default="~sqlalchemy.pool.QueuePool")

    DYNAMODB_REPOSITORY = config("DYNAMODB_REPOSITORY", cast=bool, default=False)

    # TODO: set default=None on production
    DYNAMODB_ENDPOINT = config(
        "DYNAMODB_ENDPOINT",
        cast=str,
        default=None,
    )

    DYNAMODB_REGION = config(
        "DYNAMODB_REGION",
        cast=str,
        default="eu-west-1",
    )

    AWS_COGNITO_USER_POOL_ID: str = config(
        "AWS_COGNITO_USER_POOL_ID",
        cast=str,
        default=None,
    )

    AWS_COGNITO_USER_POOL_REGION: str = config(
        "AWS_COGNITO_USER_POOL_REGION",
        cast=str,
        default=None,
    )

    AWS_COGNITO_JWKS_URL_TEMPLATE: str = config(
        "AWS_COGNITO_JWKS_URL_TEMPLATE",
        cast=str,
        default="https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json",
    )

    AWS_COGNITO_JWKS_CACHE_INTERVAL_MINUTES: int = config(
        "AWS_COGNITO_JWKS_CACHE_INTERVAL_MINUTES",
        cast=int,
        default=20,
    )
    AWS_COGNITO_JWKS_CACHE_USAGES: int = config(
        "AWS_COGNITO_JWKS_CACHE_USAGES",
        cast=int,
        default=1000,
    )

    AWS_COGNITO_USER_POOL_CLIENT_ID: str = config(
        "AWS_COGNITO_USER_POOL_CLIENT_ID",
        cast=str,
        default=None,
    )

    AWS_COGNITO_USER_POOL_CLIENT_SECRET: str = config(
        "AWS_COGNITO_USER_POOL_CLIENT_SECRET",
        cast=str,
        default=None,
    )

    # Disable authentication for the whole application
    AUTH_DISABLED = config("AUTH_DISABLED", cast=bool, default=False)


settings = Settings()
