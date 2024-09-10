from typing import List, Optional

from automapper import mapper
from sqlalchemy import delete, desc, select, text, update
from sqlalchemy.exc import IntegrityError

from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.core.repository.manager.sqlalchemy.database import Database
from web_api_template.domain.entities import Person, PersonFilter
from web_api_template.domain.repository import PersonReadRepository
from web_api_template.infrastructure.models.sqlalchemy import PersonModel


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

        # async with Database.get_db_session(self._label) as session:
        async with Database.get_db_session(self._label) as session:
            try:
                # TODO: Apply filters

                result = await session.execute(select(PersonModel))
                # It is done this way while I am creating the unit tests
                scalars = result.scalars()
                items = scalars.all()
                return [mapper.map(item, Person) for item in items]

            except Exception as ex:
                logger.exception("Database error")
                raise ex

    async def __get_by_id(self, id: str) -> PersonModel | None:
        """Get person model by ID

        Args:
            id (str): _description_

        Returns:
            PersonModel: _description_
        """
        async with Database.get_db_session(self._label) as session:
            try:
                result = await session.execute(
                    select(PersonModel).where(PersonModel.id == id)
                )
                return result.scalar_one_or_none()

            except Exception as ex:
                logger.exception("Database error")
                raise ex

    async def get_by_id(self, id: str) -> Person:
        """Gets person by id

        Args:
            id: str

        Returns:
            Person
        """

        try:
            entity_model: Optional[PersonModel] = await self.__get_by_id(id)

            if not entity_model:
                logger.debug("Item with id: {} not found", id)
                raise ItemNotFoundException(f"Item with id: {id} not found")

            return mapper.map(entity_model, Person)

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
