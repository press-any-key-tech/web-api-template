from typing import List, Optional

from automapper import mapper
from sqlalchemy import delete, desc, select, text, update
from sqlalchemy.exc import IntegrityError

from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.core.repository.manager.sqlalchemy.database import Database
from web_api_template.domain.entities import Address, AddressFilter
from web_api_template.domain.repository import AddressReadRepository
from web_api_template.infrastructure.models.sqlalchemy import AddressModel


class AddressReadRepositoryImpl(AddressReadRepository):
    """Repository implementation for Address"""

    async def get_list(
        self,
        *,
        filter: AddressFilter,
        # query: CommonQueryModel,
        # current_user: User,
    ) -> List[Address]:
        """Gets filtered policies

        Args:
            request (Request): request (from fastAPI)
            current_user (AuthUser, optional): Current user who makes the request
            filter: parameter to search (owner_id)
            query: parameter in pagination(page, size, sort)

        Returns:
            dict
        """

        logger.debug("filter: %s", filter)
        # logger.debug("query: %s", query)

        async with Database.get_db_session(self._label) as session:
            try:
                # TODO: Apply filters

                result = await session.execute(select(AddressModel))
                # It is done this way while I am creating the unit tests
                scalars = result.scalars()
                items = scalars.all()
                return [mapper.to(Address).map(item) for item in items]

            except Exception as ex:
                logger.exception("Database error")
                raise ex

    async def get_list_by_person_id(
        self,
        *,
        id: str,
        # query: CommonQueryModel,
        # current_user: User,
    ) -> List[Address]:
        """Gets filtered policies

        Args:
            request (Request): request (from fastAPI)
            current_user (AuthUser, optional): Current user who makes the request
            id: person id
            query: parameter in pagination(page, size, sort)

        Returns:
            dict
        """

        logger.debug("Person id: %s", id)
        # logger.debug("query: %s", query)

        async with Database.get_db_session(self._label) as session:
            try:

                result = await session.execute(
                    select(AddressModel).where(AddressModel.person_id == id)
                )
                # It is done this way while I am creating the unit tests
                scalars = result.scalars()
                items = scalars.all()
                return [mapper.to(Address).map(item) for item in items]

            except Exception as ex:
                logger.exception("Database error")
                raise ex

    async def __get_by_id(self, id: str) -> AddressModel | None:
        """Get address model by ID

        Args:
            id (str): _description_

        Returns:
            AddressModel: _description_
        """
        async with Database.get_db_session(self._label) as session:
            try:
                result = await session.execute(
                    select(AddressModel).where(AddressModel.id == id)
                )
                return result.scalar_one_or_none()

            except Exception as ex:
                logger.exception("Database error")
                raise ex

    async def get_by_id(self, id: str) -> Address:
        """Gets address by id

        Args:
            id: str

        Returns:
            Address
        """

        try:
            entity_model: Optional[AddressModel] = await self.__get_by_id(id)

            if not entity_model:
                logger.debug("Item with id: %s not found", id)
                raise ItemNotFoundException(f"Item with id: {id} not found")

            return mapper.to(Address).map(entity_model)

        except Exception as ex:
            logger.exception("Database error")
            raise ex
