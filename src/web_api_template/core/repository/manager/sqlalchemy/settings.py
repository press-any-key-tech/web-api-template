import json
import os
import re
from typing import Dict, List, Set

from starlette.config import Config

from web_api_template.core.repository.exceptions import SettingsNotFoundException
from web_api_template.core.settings import Settings

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
            raise SettingsNotFoundException(
                f"Label {label} not found on engine settings."
            )
        return self._settings[label]


settings = ModuleSettings()
