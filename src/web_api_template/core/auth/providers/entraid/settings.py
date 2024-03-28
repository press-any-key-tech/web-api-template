import json
import os
import re
from typing import Dict, List, Optional

from starlette.config import Config

from ...settings import ModuleSettings as Settings

config = Config()


class ModuleSettings(Settings):
    """Settings for the module"""

    AZURE_ENTRA_ID_TENANT_ID: Optional[str] = config(
        "AZURE_ENTRA_ID_TENANT_ID",
        cast=str,
        default=None,
    )

    # The audience id is the client id of the application
    AZURE_ENTRA_ID_AUDIENCE_ID: Optional[str] = config(
        "AZURE_ENTRA_ID_AUDIENCE_ID",
        cast=str,
        default=None,
    )

    AZURE_ENTRA_ID_JWKS_URL_TEMPLATE: str = config(
        "AZURE_ENTRA_ID_JWKS_URL_TEMPLATE",
        cast=str,
        default="https://login.microsoftonline.com/{}/v2.0/.well-known/openid-configuration",
    )


settings = ModuleSettings()
