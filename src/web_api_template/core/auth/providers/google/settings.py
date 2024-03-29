import json
import os
import re
from typing import Dict, List, Optional

from starlette.config import Config

from ...settings import ModuleSettings as Settings

config = Config()


class ModuleSettings(Settings):
    """Settings for the module"""

    # The audience id is the google project id
    GOOGLE_IDP_AUDIENCE_ID: Optional[str] = config(
        "GOOGLE_IDP_AUDIENCE_ID",
        cast=str,
        default=None,
    )

    # API key from the provider
    GOOGLE_IDP_API_KEY: Optional[str] = config(
        "GOOGLE_IDP_API_KEY",
        cast=str,
        default=None,
    )

    # JWT keys from google IdP are issued by firebase
    FIREBASE_JWKS_URL_TEMPLATE: str = config(
        "FIREBASE_JWKS_URL_TEMPLATE",
        cast=str,
        default="https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com",
    )


settings = ModuleSettings()
