from abc import ABCMeta, abstractmethod
from typing import List, Optional

from web_api_template.domain.entities import Address, AddressFilter
from web_api_template.core.repository.manager.sqlalchemy.repository_base import RepositoryBase

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
    async def get_list_by_person_id(self, *, id: str) -> List[Address]:
        raise NotImplementedError()
