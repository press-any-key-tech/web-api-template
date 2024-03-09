import json
import os
import re
from typing import Dict, List

from starlette.config import Config

from web_api_template.core.settings import Settings

config = Config()


class ModuleSettings(Settings):
    """Settings for the module"""

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


settings = ModuleSettings()
