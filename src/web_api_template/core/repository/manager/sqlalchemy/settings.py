import json
import os
import re
from typing import Dict, List

from starlette.config import Config

from web_api_template.core.settings import Settings

config = Config()


class ModuleSettings(Settings):
    """Settings for the module"""

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


settings = ModuleSettings()
