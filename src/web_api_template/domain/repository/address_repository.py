from abc import ABCMeta, abstractmethod
from typing import List, Optional

from web_api_template.domain.entities import Address, AddressFilter


class AddressRepository(metaclass=ABCMeta):
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

    @abstractmethod
    async def create(self, *, entity: Address) -> Optional[Address]:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, *, id: str, address: Address) -> Optional[Address]:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, *, id: str):
        return NotImplementedError()
