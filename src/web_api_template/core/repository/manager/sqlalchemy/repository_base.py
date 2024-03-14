from abc import ABCMeta, abstractmethod
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from web_api_template.core.repository.manager.sqlalchemy.database import Database


class RepositoryBase(metaclass=ABCMeta):
    """
    Abstract class for database repository

    Raises:
        NotImplementedError: _description_
    """

    _session: AsyncSession
    _label: str

    def __init__(self, label: str = "DEFAULT"):
        """Initialize the repository

        Args:
            label (str, optional): label for the configuration to recover. Defaults to 'DEFAULT'.
        """
        self._session = Database.get_db_session(label)
        self._label = label

    # @staticmethod
    # @asynccontextmanager
    # async def get_db_session(label: str = "DEFAULT"):
    #     """Gets a session from database

    #     Yields:
    #         _type_: _description_
    #     """
    #     # Async session returns a sessión factory (sessionmaker) and it needs () to create a session
    #     async with Database().async_session(label)() as session:
    #         yield session
