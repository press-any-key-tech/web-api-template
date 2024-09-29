from abc import abstractmethod
from typing import List, Optional

from web_api_template.core.repository.manager.sqlalchemy.repository_base import (
    RepositoryBase,
)
from web_api_template.domain.aggregates import Policy, PolicyFilter


class PolicyReadRepository(RepositoryBase):
    """
    Abstract class for database policy repository

    Raises:
        NotImplementedError: _description_
    """

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Policy]:
        raise NotImplementedError()

    @abstractmethod
    async def get_list(self, *, filter: PolicyFilter) -> List[Policy]:
        raise NotImplementedError()

    @abstractmethod
    async def get_list_by_person_id(self, *, person_id: str) -> List[Policy]:
        raise NotImplementedError()
