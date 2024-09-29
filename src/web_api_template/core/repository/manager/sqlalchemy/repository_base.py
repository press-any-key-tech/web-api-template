from abc import ABCMeta, abstractmethod
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from web_api_template.core.repository.manager.sqlalchemy.async_database import (
    AsyncDatabase,
)


class RepositoryBase(metaclass=ABCMeta):
    """
    Abstract class for database repository

    Raises:
        NotImplementedError: _description_
    """

    _label: str

    def __init__(self, label: str = "DEFAULT"):
        """Initialize the repository

        Args:
            label (str, optional): label for the configuration to recover. Defaults to 'DEFAULT'.
        """
        self._label = label
