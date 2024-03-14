import json
import os
import re
from typing import Dict, List, Set

from starlette.config import Config

from web_api_template.core.settings import Settings
from web_api_template.core.repository.exceptions import SettingsNotFoundException

from .db_engines_enum import DbEnginesEnum
from .engine_settings import EngineSettings

config = Config()


class ModuleSettings(Settings):
    """SqlAlchemy settings
    Env variable format: SQLALCHEMY__<LABEL>__<PARAMETER>
    Where:
        LABEL: label of the database parameter
        PARAMETER: parameter to configure
    Example:
        SQLALCHEMY__DEFAULT__SQLALCHEMY_DATABASE_URI

    Args:
        Settings (_type_): _description_
    """

    __prefix: str = "SQLALCHEMY__"
    _settings: Dict[str, EngineSettings]
    _labels: List[str]

    def __init__(self):
        self._settings = {}
        self.config = Config()

        env_vars: List[str] = [
            var for var in os.environ if var.startswith(self.__prefix)
        ]

        labels: Set[str] = set([element.split("__")[1] for element in env_vars])
        self._labels = list(labels)

        self._settings = {
            label: EngineSettings(label=label, prefix=self.__prefix) for label in labels
        }


    @property
    def labels(self):
        return self._labels

    def get_settings(self, label: str) -> EngineSettings:
        """Get settings for a given label
        TODO: Always have a default label

        Args:
            label (str): label to get settings

        Returns:
            EngineSettings: settings for the given label
        """
        if label not in self._settings:
            raise SettingsNotFoundException(f"Label {label} not found on engine settings.")
        return self._settings[label]

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
