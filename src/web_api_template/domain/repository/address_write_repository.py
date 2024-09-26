from abc import ABCMeta, abstractmethod
from typing import List, Optional

from web_api_template.core.repository.manager.sqlalchemy.repository_base import (
    RepositoryBase,
)
from web_api_template.domain.value_objects import Address, AddressBase, AddressFilter


class AddressWriteRepository(RepositoryBase):
    """
    Abstract class for database address repository

    Raises:
        NotImplementedError: _description_
    """

    @abstractmethod
    async def create(self, *, person_id: str, entity: Address) -> Optional[Address]:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, *, id: str, address: AddressBase) -> Optional[AddressBase]:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, *, id: str):
        return NotImplementedError()
