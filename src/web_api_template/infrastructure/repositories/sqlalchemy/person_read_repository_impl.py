from typing import Optional

from automapper import mapper
from sqlalchemy import select

from web_api_template.core.api.pagination_query_model import PaginationQueryModel
from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.core.repository.manager.sqlalchemy.async_database import (
    AsyncDatabase,
)
from web_api_template.core.repository.manager.sqlalchemy.async_paginator import (
    AsyncPaginator,
)
from web_api_template.core.repository.manager.sqlalchemy.page import Page
from web_api_template.domain.entities.person import Person
from web_api_template.domain.entities.person_filter import PersonFilter
from web_api_template.domain.repository import PersonReadRepository
from web_api_template.infrastructure.models.sqlalchemy import PersonModel


class PersonReadRepositoryImpl(PersonReadRepository):
    """Repository implementation for Person"""

    async def get_paginated_list(
        self,
        *,
        filter: PersonFilter,
        pagination: PaginationQueryModel,
        # current_user: User,
    ) -> Page:
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

        # async with AsyncDatabase.get_session(self._label) as session:
        async with AsyncDatabase.get_session(self._label) as session:
            try:

                result: Page = await AsyncPaginator(session).list(
                    model=PersonModel,
                    page=pagination.page,
                    size=pagination.size,
                    order_by=pagination.sort.split(",") if pagination.sort else [],
                )

                result.items = [mapper.map(item, Person) for item in result.items]
                return result

            except Exception as ex:
                logger.exception("AsyncDatabase error")
                raise ex

    async def __get_by_id(self, id: str) -> PersonModel | None:
        """Get person model by ID

        Args:
            id (str): _description_

        Returns:
            PersonModel: _description_
        """

        async with AsyncDatabase.get_session(self._label) as session:
            try:
                # result = await session.execute(
                #     select(PersonModel)
                #     .where(PersonModel.id == id)
                #     .options(
                #         selectinload(PersonModel.addresses),
                #         selectinload(PersonModel.policies),
                #     )
                # )

                result = await session.execute(
                    select(PersonModel).where(PersonModel.id == id)
                )

                return result.scalar_one_or_none()

            except Exception as ex:
                logger.exception("AsyncDatabase error")
                raise ex

    async def get_by_id(self, id: str) -> Person:
        """Gets person by id

        Args:
            id: str

        Returns:
            Person
        """

        entity_model: Optional[PersonModel] = await self.__get_by_id(id)

        if not entity_model:
            logger.debug("Item with id: {} not found", id)
            raise ItemNotFoundException(f"Item with id: {id} not found")

        return mapper.map(entity_model, Person)

    # async def count_Persons(self) -> int:
    #     with DbConnectionManager() as manager:
    #         search_db: int = (
    #             manager.session.query(PersonModel)
    #             .filter(PersonModel.deleted == False)
    #             .count()
    #         )

    #         return search_db
