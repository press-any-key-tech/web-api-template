from typing import List, Optional

from automapper import mapper
from sqlalchemy import delete, desc, select, text, update
from sqlalchemy.exc import IntegrityError

from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.core.repository.manager.sqlalchemy.database import Database
from web_api_template.domain.entities import Content, ContentFilter
from web_api_template.domain.repository import ContentReadRepository
from web_api_template.infrastructure.models.sqlalchemy import ContentModel


class ContentReadRepositoryImpl(ContentReadRepository):
    """Repository implementation for Content"""

    async def get_list(
        self,
        *,
        filter: ContentFilter,
        # query: CommonQueryModel,
        # current_user: User,
    ) -> List[Content]:
        """Gets filtered policies

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

        async with Database.get_db_session(self._label) as session:
            try:
                # TODO: Apply filters

                result = await session.execute(select(ContentModel))
                # It is done this way while I am creating the unit tests
                scalars = result.scalars()
                items = scalars.all()
                return [mapper.to(Content).map(item) for item in items]

            except Exception as ex:
                logger.exception("Database error")
                raise ex

    async def get_list_by_policy_id(
        self,
        *,
        id: str,
        # query: CommonQueryModel,
        # current_user: User,
    ) -> List[Content]:
        """Gets filtered contents

        Args:
            request (Request): request (from fastAPI)
            current_user (AuthUser, optional): Current user who makes the request
            id: policy id
            query: parameter in pagination(page, size, sort)

        Returns:
            dict
        """

        logger.debug("Person id: {}", id)
        # logger.debug("query: %s", query)

        async with Database.get_db_session(self._label) as session:
            try:

                result = await session.execute(
                    select(ContentModel).where(ContentModel.policy_id == id)
                )
                # It is done this way while I am creating the unit tests
                scalars = result.scalars()
                items = scalars.all()
                return [mapper.to(Content).map(item) for item in items]

            except Exception as ex:
                logger.exception("Database error")
                raise ex

    async def __get_by_id(self, id: str) -> ContentModel | None:
        """Get content model by ID

        Args:
            id (str): _description_

        Returns:
            ContentModel: _description_
        """
        async with Database.get_db_session(self._label) as session:
            try:
                result = await session.execute(
                    select(ContentModel).where(ContentModel.id == id)
                )
                return result.scalar_one_or_none()

            except Exception as ex:
                logger.exception("Database error")
                raise ex

    async def get_by_id(self, id: str) -> Content:
        """Gets content by id

        Args:
            id: str

        Returns:
            Content
        """

        try:
            entity_model: Optional[ContentModel] = await self.__get_by_id(id)

            if not entity_model:
                logger.debug("Item with id: {} not found", id)
                raise ItemNotFoundException(f"Item with id: {id} not found")

            return mapper.to(Content).map(entity_model)

        except Exception as ex:
            logger.exception("Database error")
            raise ex
