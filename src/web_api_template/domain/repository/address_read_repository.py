from abc import abstractmethod
from typing import List, Optional

from web_api_template.core.repository.manager.sqlalchemy.repository_base import (
    RepositoryBase,
)
from web_api_template.domain.value_objects import Address, AddressFilter


class AddressReadRepository(RepositoryBase):
    """
    Abstract class for database address repository

    Raises:
        NotImplementedError: _description_
    """

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Address]:
        raise NotImplementedError()

    @abstractmethod
    async def get_list(self, *, filter: AddressFilter) -> List[Address]:
        raise NotImplementedError()

    @abstractmethod
    async def get_list_by_person_id(self, *, person_id: str) -> List[Address]:
        raise NotImplementedError()
