from typing import List

from web_api_template.core.di_injector import inject
from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.domain.entities import Person, PersonFilter
from web_api_template.domain.exceptions import PersonNotFoundException
from web_api_template.domain.repository import PersonRepository


class ReadService:
    """Query operations"""

    @inject()
    def __init__(self, person_db_repo: PersonRepository):
        self.person_db_repo = person_db_repo

    async def get_list(self, filter: PersonFilter) -> List[Person]:
        """
        Get a list of persons

        Args:
            filter (PersonFilter): Person related filter

        Returns:
            List[Person]: domain entity to return
        """

        logger.debug("Entering. filter: %s", filter)

        entities: List[Person] = await self.person_db_repo.get_list(filter=filter)

        return entities

    async def get_by_id(self, id: str) -> Person:
        """
        Search person by id

        Args:
            id (str): id of the person

        Returns:
            person: domain entity to return
        """

        logger.debug("Entering. id: %s", id)

        try:
            entity: Person | None = await self.person_db_repo.get_by_id(id=id)
        except ItemNotFoundException:
            # Domain exception raise if pot doesn't exists
            raise PersonNotFoundException(f"Person with id [{id}] not found")

        return entity
