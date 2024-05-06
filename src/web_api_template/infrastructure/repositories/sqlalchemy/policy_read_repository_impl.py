from typing import List, Optional

from automapper import mapper
from sqlalchemy import delete, desc, select, text, update
from sqlalchemy.exc import IntegrityError

from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.core.repository.manager.sqlalchemy.database import Database
from web_api_template.domain.entities import Policy, PolicyFilter
from web_api_template.domain.repository import PolicyReadRepository
from web_api_template.infrastructure.models.sqlalchemy import PolicyModel


class PolicyReadRepositoryImpl(PolicyReadRepository):
    """Repository implementation for Policy"""

    async def get_list(
        self,
        *,
        filter: PolicyFilter,
        # query: CommonQueryModel,
        # current_user: User,
    ) -> List[Policy]:
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

                result = await session.execute(select(PolicyModel))
                # It is done this way while I am creating the unit tests
                scalars = result.scalars()
                items = scalars.all()
                return [mapper.to(Policy).map(item) for item in items]

            except Exception as ex:
                logger.exception("Database error")
                raise ex

    async def get_list_by_person_id(
        self,
        *,
        id: str,
        # query: CommonQueryModel,
        # current_user: User,
    ) -> List[Policy]:
        """Gets filtered policies

        Args:
            request (Request): request (from fastAPI)
            current_user (AuthUser, optional): Current user who makes the request
            id: person id
            query: parameter in pagination(page, size, sort)

        Returns:
            dict
        """

        logger.debug("Person id: {}", id)
        # logger.debug("query: %s", query)

        async with Database.get_db_session(self._label) as session:
            try:

                result = await session.execute(
                    select(PolicyModel).where(PolicyModel.person_id == id)
                )
                # It is done this way while I am creating the unit tests
                scalars = result.scalars()
                items = scalars.all()
                return [mapper.to(Policy).map(item) for item in items]

            except Exception as ex:
                logger.exception("Database error")
                raise ex

    async def __get_by_id(self, id: str) -> PolicyModel | None:
        """Get policy model by ID

        Args:
            id (str): _description_

        Returns:
            PolicyModel: _description_
        """
        async with Database.get_db_session(self._label) as session:
            try:
                result = await session.execute(
                    select(PolicyModel).where(PolicyModel.id == id)
                )
                return result.scalar_one_or_none()

            except Exception as ex:
                logger.exception("Database error")
                raise ex

    async def get_by_id(self, id: str) -> Policy:
        """Gets policy by id

        Args:
            id: str

        Returns:
            Policy
        """

        try:
            entity_model: Optional[PolicyModel] = await self.__get_by_id(id)

            if not entity_model:
                logger.debug("Item with id: {} not found", id)
                raise ItemNotFoundException(f"Item with id: {id} not found")

            return mapper.to(Policy).map(entity_model)

        except Exception as ex:
            logger.exception("Database error")
            raise ex
