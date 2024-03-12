from abc import ABCMeta, abstractmethod
from typing import List, Optional

from web_api_template.domain.entities import Address, AddressFilter


class AddressWriteRepository(metaclass=ABCMeta):
    """
    Abstract class for database address repository

    Raises:
        NotImplementedError: _description_
    """

    @abstractmethod
    async def create(self, *, entity: Address) -> Optional[Address]:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, *, id: str, address: Address) -> Optional[Address]:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, *, id: str):
        return NotImplementedError()
