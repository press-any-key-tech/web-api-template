from typing import List, Optional

from automapper import mapper

from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.domain.entities.person import Person
from web_api_template.domain.entities.person_create import PersonCreate
from web_api_template.domain.entities.person_filter import PersonFilter
from web_api_template.domain.repository import PersonReadRepository
from web_api_template.infrastructure.models.dynamodb import PersonModel


class PersonReadRepositoryImpl(PersonReadRepository):
    """Repository implementation for Person"""

    async def get_list(
        self,
        *,
        filter: PersonFilter,
        # query: CommonQueryModel,
        # current_user: User,
    ) -> List[Person]:
        """Gets filtered persons

        Args:
            request (Request): request (from fastAPI)
            current_user (AuthUser, optional): Current user who makes the request
            filter: parameter to search (owner_id)
            query: parameter in pagination(page, size, sort)

        Returns:
            dict
        """

        logger.debug("filter: {}", filter)
        # logger.debug("query: %s", query)

        try:
            return [mapper.map(item, Person) for item in PersonModel.scan()]

        except Exception as ex:
            logger.exception("Database error reading persons: {}", ex)
            raise ex

    async def get_by_id(self, id: str) -> Person:
        """Gets person by id

        Args:
            id: str

        Returns:
            Person
        """

        try:
            entity_model: PersonModel = PersonModel.get(id)

            if not entity_model:
                logger.debug("Item with id: {} not found", id)
                raise ItemNotFoundException(f"Item with id: {id} not found")

            return mapper.map(entity_model, Person)

        except PersonModel.DoesNotExist as nex:
            logger.exception("Item does not exists")
            raise ItemNotFoundException(f"Item with id: {id} not found")

        except Exception as ex:
            logger.exception("Database error")
            raise ex

    # async def count_Persons(self) -> int:
    #     with DbConnectionManager() as manager:
    #         search_db: int = (
    #             manager.session.query(PersonModel)
    #             .filter(PersonModel.deleted == False)
    #             .count()
    #         )

    #         return search_db
