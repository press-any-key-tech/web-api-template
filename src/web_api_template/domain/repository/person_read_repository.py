from abc import ABCMeta, abstractmethod
from typing import List, Optional

from web_api_template.core.repository.manager.sqlalchemy.repository_base import (
    RepositoryBase,
)
from web_api_template.domain.entities import Person, PersonFilter


class PersonReadRepository(RepositoryBase):
    """
    Abstract class for database person repository

    Raises:
        NotImplementedError: _description_
    """

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Person]:
        raise NotImplementedError()

    @abstractmethod
    async def get_list(self, *, filter: PersonFilter) -> List[Person]:
        raise NotImplementedError()

    # @abstractmethod
    # async def get_list(self, *, filter: PersonsFilter, query: CommonQueryModel) -> dict:
    #     raise NotImplementedError()
