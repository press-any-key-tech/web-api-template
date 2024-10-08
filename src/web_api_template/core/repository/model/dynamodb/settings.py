
from starlette.config import Config

from web_api_template.core.settings import Settings

config = Config()


class ModuleSettings(Settings):
    """Settings for the module"""

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


settings = ModuleSettings()
