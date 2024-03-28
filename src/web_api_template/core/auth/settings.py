import json
import os
import re
from typing import Dict, List

from starlette.config import Config

from web_api_template.core.settings import Settings

config = Config()


class ModuleSettings(Settings):
    """Settings for the module"""

    # Disable authentication for the whole application
    AUTH_DISABLED = config("AUTH_DISABLED", cast=bool, default=False)

    AUTH_JWKS_CACHE_INTERVAL_MINUTES: int = config(
        "AUTH_JWKS_CACHE_INTERVAL_MINUTES",
        cast=int,
        default=20,
    )
    AUTH_JWKS_CACHE_USAGES: int = config(
        "AUTH_JWKS_CACHE_USAGES",
        cast=int,
        default=1000,
    )


settings = ModuleSettings()
