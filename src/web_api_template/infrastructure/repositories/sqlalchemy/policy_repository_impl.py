from typing import List, Optional

from automapper import mapper
from sqlalchemy import delete, desc, select, text, update
from sqlalchemy.exc import IntegrityError

from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.core.repository.manager.sqlalchemy.database import Database
from web_api_template.domain.entities import Policy, PolicyFilter
from web_api_template.domain.repository import PolicyRepository
from web_api_template.infrastructure.models.sqlalchemy import PolicyModel


class PolicyRepositoryImpl(PolicyRepository):
    """Repository implementation for Policy"""

    _model = PolicyModel

    async def create(
        self,
        *,
        # current_user: User,
        entity: Policy,
    ) -> Policy:
        """
        Create a policy on DB

        Args:
            entity (policy): policy to create
        Returns:
            policy (policy): policy created
        """

        entity_model: PolicyModel = mapper.to(PolicyModel).map(entity)

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

            return mapper.to(Policy).map(entity_model)

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

        logger.debug("filter: %s", filter)
        # logger.debug("query: %s", query)

        async with Database.get_db_session() as session:
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

        logger.debug("Person id: %s", id)
        # logger.debug("query: %s", query)

        async with Database.get_db_session() as session:
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
        async with Database.get_db_session() as session:
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
            entity_model: PolicyModel = await self.__get_by_id(id)

            if not entity_model:
                logger.debug("Item with id: %s not found", id)
                raise ItemNotFoundException(f"Item with id: {id} not found")

            return mapper.to(Policy).map(entity_model)

        except Exception as ex:
            logger.exception("Database error")
            raise ex

    async def __delete(self, id: str) -> None:
        """Delete policy model by ID

        Args:
            id (str): _description_

        Returns:
            None

        """
        async with Database.get_db_session() as session:
            try:
                delete_query = delete(PolicyModel).where(PolicyModel.id == id)
                await session.execute(delete_query)
                await session.commit()
                return

            except Exception as ex:
                logger.exception("Database error")
                raise ex

    async def delete(self, id: str) -> None:
        """Delete policy by id

        Args:
            request (Request): request (from fastAPI)
            id: str

        Returns:
            None
        """

        try:
            entity_model: PolicyModel = await self.__get_by_id(id)

            if not entity_model:
                # TODO : check if policy is in delete status
                logger.debug("Item with id: %s not found", id)
                raise ItemNotFoundException(f"Item with id: {id} not found")

            # Delete the given (and existing) id
            await self.__delete(id)

        except Exception as ex:
            logger.exception("Database error")
            raise ex

    async def __update(self, id: str, model: PolicyModel) -> PolicyModel:
        """update policy model with the given ID

        Args:
            id (str): _description_

        Returns:
            PolicyModel

        """

        # TODO: concurrency fields
        # model.updated_at = datetime.utcnow()
        # model.updated_by = "fake"

        async with Database.get_db_session() as session:
            try:
                # Vuild the update query
                update_query = (
                    update(PolicyModel)
                    .where(PolicyModel.id == id)
                    .values(
                        policy_number=model.policy_number,
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
        policy: Policy,
        # current_user: User
    ) -> Optional[Policy]:
        """
        Update policy into DB
        Args:
            id (str): Template ID used to update
            policy (Policy): Policy that will be updated
        Returns:
            Policy: Policy updated
        """

        try:
            entity_model: PolicyModel = await self.__get_by_id(id)

            if not entity_model:
                # TODO : check if policy is in delete status
                logger.debug("Item with id: %s not found", id)
                raise ItemNotFoundException(f"Item with id: {id} not found")

            new_model: PolicyModel = mapper.to(PolicyModel).map(policy)

            # Update the given (and existing) id
            result: PolicyModel = await self.__update(id=id, model=new_model)

            return mapper.to(Policy).map(result)

        except Exception as ex:
            logger.exception("Database error")
            raise ex

    # async def count_Policies(self) -> int:
    #     with DbConnectionManager() as manager:
    #         search_db: int = (
    #             manager.session.query(PolicyModel)
    #             .filter(PolicyModel.deleted == False)
    #             .count()
    #         )

    #         return search_db
