from datetime import datetime
from typing import Optional

from automapper import mapper
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError

from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.core.repository.manager.sqlalchemy.async_database import (
    AsyncDatabase,
)
from web_api_template.domain.entities.person import Person
from web_api_template.domain.entities.person_create import PersonCreate
from web_api_template.domain.exceptions import (
    PersonAlreadyExistsException,
    PersonAlreadyModifiedException,
)
from web_api_template.domain.repository import PersonWriteRepository
from web_api_template.infrastructure.models.sqlalchemy import PersonModel


class PersonWriteRepositoryImpl(PersonWriteRepository):
    """Repository implementation for Person"""

    async def create(
        self,
        *,
        # current_user: User,
        entity: PersonCreate,
    ) -> PersonCreate:
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

        async with AsyncDatabase.get_session(self._label) as session:
            try:
                session.add(entity_model)
                await session.commit()
            except IntegrityError as ie:
                await session.rollback()
                logger.exception("Integrity exception, person already exists.")
                raise PersonAlreadyExistsException(entity.identification_number)
            except Exception as ex:
                await session.rollback()
                logger.exception("Commit error")
                raise ex

            return mapper.map(entity_model, PersonCreate)

    async def __get_by_id(self, id: str) -> PersonModel | None:
        """Get person model by ID

        Args:
            id (str): _description_

        Returns:
            PersonModel: _description_
        """
        async with AsyncDatabase.get_session(self._label) as session:
            try:
                result = await session.execute(
                    select(PersonModel).where(PersonModel.id == id)
                )
                return result.scalar_one_or_none()

            except Exception as ex:
                logger.exception("AsyncDatabase error")
                raise ex

    async def __delete(self, id: str) -> None:
        """Delete person model by ID

        Args:
            id (str): _description_

        Returns:
            None

        """
        async with AsyncDatabase.get_session(self._label) as session:
            try:
                delete_query = delete(PersonModel).where(PersonModel.id == id)
                await session.execute(delete_query)
                await session.commit()
                return

            except Exception as ex:
                await session.rollback()
                logger.exception("AsyncDatabase error")
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
            logger.exception("AsyncDatabase error")
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

        async with AsyncDatabase.get_session(self._label) as session:
            try:

                # TODO: change to an exists
                current_person = await session.execute(
                    select(PersonModel).where(PersonModel.id == id)
                )
                current_person = current_person.scalar_one_or_none()

                if not current_person:
                    raise ItemNotFoundException(f"Item with id: {id} not found")

                update_query = (
                    update(PersonModel)
                    .where(PersonModel.id == id)
                    .where(PersonModel.version == model.version)  # Verify version
                    .values(
                        name=model.name,
                        surname=model.surname,
                        email=model.email,
                        identification_number=model.identification_number,
                        version=model.version + 1,  # Increment version
                        updated_at=datetime.now(),
                    )
                )

                result = await session.execute(update_query)

                if result.rowcount == 0:
                    raise StaleDataError(
                        "Another transaction has modified this record."
                    )

                await session.commit()

                # return await self.__get_by_id(id)
                model.id = id
                model.version = model.version + 1

                return model

            except IntegrityError as ie:
                await session.rollback()
                logger.exception(
                    "Integrity exception, identification number already exists."
                )
                raise PersonAlreadyExistsException(model.identification_number)

            except StaleDataError as sde:
                await session.rollback()
                logger.exception(
                    "Concurrency exception, record was modified by another transaction."
                )
                raise PersonAlreadyModifiedException(id)

            except Exception as ex:
                await session.rollback()
                logger.exception("AsyncDatabase error")
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
            logger.exception("AsyncDatabase error")
            raise ex

    # async def count_Persons(self) -> int:
    #     with DbConnectionManager() as manager:
    #         search_db: int = (
    #             manager.session.query(PersonModel)
    #             .filter(PersonModel.deleted == False)
    #             .count()
    #         )

    #         return search_db
