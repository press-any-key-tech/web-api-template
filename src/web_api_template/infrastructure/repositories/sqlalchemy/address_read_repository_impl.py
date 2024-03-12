from typing import List, Optional

from automapper import mapper
from sqlalchemy import delete, desc, select, text, update
from sqlalchemy.exc import IntegrityError

from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.core.repository.manager.sqlalchemy.database import Database
from web_api_template.domain.entities import Address, AddressFilter
from web_api_template.domain.repository import AddressRepository
from web_api_template.infrastructure.models.sqlalchemy import AddressModel


class AddressReadRepositoryImpl(AddressRepository):
    """Repository implementation for Address"""

    _model = AddressModel

    async def create(
        self,
        *,
        # current_user: User,
        entity: Address,
    ) -> Address:
        """
        Create a address on DB

        Args:
            entity (address): address to create
        Returns:
            address (address): address created
        """

        entity_model: AddressModel = mapper.to(AddressModel).map(entity)

        # set_concurrency_fields(source=entity_model, user=current_user)
        # entity_model.owner_id = str(current_user.id)

        async with Database.get_db_session() as session:
            try:
                session.add(entity_model)
                await session.commit()
                await session.refresh(entity_model)
            # except IntegrityError as ie:
            #     await session.rollback()
            #     logger.exception("Integrity exception")
            #     error_info: str = str(ie.orig)
            #     detail_message: str = error_info
            #     detail_index = error_info.find("DETAIL:")
            #     if detail_index != -1:
            #         detail_message = error_info[detail_index + len("DETAIL:") :].strip()
            #     raise DuplicatedSlugException(detail_message)
            except Exception as ex:
                logger.exception("Commit error")
                raise ex

            return mapper.to(Address).map(entity_model)

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

        async with Database.get_db_session() as session:
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

        async with Database.get_db_session() as session:
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
        async with Database.get_db_session() as session:
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
            entity_model: AddressModel = await self.__get_by_id(id)

            if not entity_model:
                logger.debug("Item with id: %s not found", id)
                raise ItemNotFoundException(f"Item with id: {id} not found")

            return mapper.to(Address).map(entity_model)

        except Exception as ex:
            logger.exception("Database error")
            raise ex

    async def __delete(self, id: str) -> None:
        """Delete address model by ID

        Args:
            id (str): _description_

        Returns:
            None

        """
        async with Database.get_db_session() as session:
            try:
                delete_query = delete(AddressModel).where(AddressModel.id == id)
                await session.execute(delete_query)
                await session.commit()
                return

            except Exception as ex:
                logger.exception("Database error")
                raise ex

    async def delete(self, id: str) -> None:
        """Delete address by id

        Args:
            request (Request): request (from fastAPI)
            id: str

        Returns:
            None
        """

        try:
            entity_model: AddressModel = await self.__get_by_id(id)

            if not entity_model:
                # TODO : check if address is in delete status
                logger.debug("Item with id: %s not found", id)
                raise ItemNotFoundException(f"Item with id: {id} not found")

            # Delete the given (and existing) id
            await self.__delete(id)

        except Exception as ex:
            logger.exception("Database error")
            raise ex

    async def __update(self, id: str, model: AddressModel) -> AddressModel:
        """update address model with the given ID

        Args:
            id (str): _description_

        Returns:
            AddressModel

        """

        # TODO: concurrency fields
        # model.updated_at = datetime.utcnow()
        # model.updated_by = "fake"

        async with Database.get_db_session() as session:
            try:
                # Vuild the update query
                update_query = (
                    update(AddressModel)
                    .where(AddressModel.id == id)
                    .values(
                        address_number=model.address_number,
                        person_id=model.person_id,
                        status=model.status,
                    )
                )

                await session.execute(update_query)
                await session.commit()

                return await self.__get_by_id(id)

            except Exception as ex:
                await session.rollback()
                logger.exception("Database error")
                raise ex

    async def update(
        self,
        *,
        id: str,
        address: Address,
        # current_user: User
    ) -> Optional[Address]:
        """
        Update address into DB
        Args:
            id (str): Template ID used to update
            address (Address): Address that will be updated
        Returns:
            Address: Address updated
        """

        try:
            entity_model: AddressModel = await self.__get_by_id(id)

            if not entity_model:
                # TODO : check if address is in delete status
                logger.debug("Item with id: %s not found", id)
                raise ItemNotFoundException(f"Item with id: {id} not found")

            new_model: AddressModel = mapper.to(AddressModel).map(address)

            # Update the given (and existing) id
            result: AddressModel = await self.__update(id=id, model=new_model)

            return mapper.to(Address).map(result)

        except Exception as ex:
            logger.exception("Database error")
            raise ex

    # async def count_Policies(self) -> int:
    #     with DbConnectionManager() as manager:
    #         search_db: int = (
    #             manager.session.query(AddressModel)
    #             .filter(AddressModel.deleted == False)
    #             .count()
    #         )

    #         return search_db
