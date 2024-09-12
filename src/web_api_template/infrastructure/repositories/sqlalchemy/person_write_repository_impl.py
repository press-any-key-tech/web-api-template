from typing import List, Optional

from automapper import mapper
from sqlalchemy import delete, desc, select, text, update
from sqlalchemy.exc import IntegrityError

from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.core.repository.manager.sqlalchemy.database import Database
from web_api_template.domain.entities import Person, PersonCreate, PersonFilter
from web_api_template.domain.repository import PersonWriteRepository
from web_api_template.infrastructure.models.sqlalchemy import PersonModel


class PersonWriteRepositoryImpl(PersonWriteRepository):
    """Repository implementation for Person"""

    async def create(
        self,
        *,
        # current_user: User,
        entity: PersonCreate,
    ) -> Person:
        """
        Create a person on DB

        Args:
            entity (person): person to create
        Returns:
            person (person): person created
        """

        entity_model: PersonModel = mapper.map(entity, PersonModel)

        # set_concurrency_fields(source=entity_model, user=current_user)
        # entity_model.owner_id = str(current_user.id)

        async with Database.get_db_session(self._label) as session:
            try:
                session.add(entity_model)
                await session.commit()
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
                await session.rollback()
                logger.exception("Commit error")
                raise ex

            return mapper.map(entity_model, Person)

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

    async def __delete(self, id: str) -> None:
        """Delete person model by ID

        Args:
            id (str): _description_

        Returns:
            None

        """
        async with Database.get_db_session(self._label) as session:
            try:
                delete_query = delete(PersonModel).where(PersonModel.id == id)
                await session.execute(delete_query)
                await session.commit()
                return

            except Exception as ex:
                await session.rollback()
                logger.exception("Database error")
                raise ex

    async def delete(self, id: str) -> None:
        """Delete person by id

        Args:
            request (Request): request (from fastAPI)
            id: str

        Returns:
            None
        """

        try:
            entity_model: Optional[PersonModel] = await self.__get_by_id(id)

            if not entity_model:
                # TODO : check if person is in delete status
                logger.debug("Item with id: {} not found", id)
                raise ItemNotFoundException(f"Item with id: {id} not found")

            # Delete the given (and existing) id
            await self.__delete(id)

        except Exception as ex:
            logger.exception("Database error")
            raise ex

    async def __update(self, id: str, model: PersonModel) -> Optional[PersonModel]:
        """update person model with the given ID

        Args:
            id (str): _description_

        Returns:
            PersonModel

        """

        # TODO: concurrency fields
        # model.updated_at = datetime.utcnow()
        # model.updated_by = "fake"

        async with Database.get_db_session(self._label) as session:
            try:
                # Vuild the update query
                update_query = (
                    update(PersonModel)
                    .where(PersonModel.id == id)
                    .values(
                        name=model.name,
                        surname=model.surname,
                        email=model.email,
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
        person: Person,
        # current_user: User
    ) -> Optional[Person]:
        """
        Update person into DB
        Args:
            id (str): Template ID used to update
            person (Person): Person that will be updated
        Returns:
            Person: Person updated
        """

        try:
            entity_model: Optional[PersonModel] = await self.__get_by_id(id)

            if not entity_model:
                # TODO : check if person is in delete status
                logger.debug("Item with id: {} not found", id)
                raise ItemNotFoundException(f"Item with id: {id} not found")

            new_model: PersonModel = mapper.map(person, PersonModel)

            # Update the given (and existing) id
            result: Optional[PersonModel] = await self.__update(id=id, model=new_model)

            return mapper.map(result, Person)

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
