from abc import abstractmethod
from typing import Optional

from web_api_template.core.repository.manager.sqlalchemy.repository_base import (
    RepositoryBase,
)
from web_api_template.domain.entities.person import Person
from web_api_template.domain.entities.person_create import PersonCreate


class PersonWriteRepository(RepositoryBase):
    """
    Abstract class for database person repository

    Raises:
        NotImplementedError: _description_
    """

    @abstractmethod
    async def create(self, *, entity: PersonCreate) -> Optional[Person]:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, *, id: str, person: Person) -> Optional[Person]:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, *, id: str):
        return NotImplementedError()
