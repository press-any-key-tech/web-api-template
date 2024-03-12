from abc import ABCMeta, abstractmethod
from typing import List, Optional

from web_api_template.domain.entities import Person, PersonFilter


class PersonWriteRepository(metaclass=ABCMeta):
    """
    Abstract class for database person repository

    Raises:
        NotImplementedError: _description_
    """

    @abstractmethod
    async def create(self, *, entity: Person) -> Optional[Person]:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, *, id: str, person: Person) -> Optional[Person]:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, *, id: str):
        return NotImplementedError()
