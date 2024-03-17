from abc import ABCMeta, abstractmethod

from web_api_template.core.repository.manager.sqlalchemy.repository_base import (
    RepositoryBase,
)


class HealthcheckRepository(RepositoryBase):
    """
    Abstract class for database repository

    Raises:
        NotImplementedError: _description_
    """

    @abstractmethod
    async def verify(self) -> bool:
        raise NotImplementedError()
