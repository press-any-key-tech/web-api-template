from abc import ABCMeta, abstractmethod
from typing import List, Optional

from web_api_template.domain.entities import Person, PersonFilter


class PersonRepository(metaclass=ABCMeta):
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

    @abstractmethod
    async def create(self, *, entity: Person) -> Optional[Person]:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, *, id: str, person: Person) -> Optional[Person]:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, *, id: str):
        return NotImplementedError()
