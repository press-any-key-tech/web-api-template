from typing import Optional

from automapper import mapper

from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.domain.entities.person import Person
from web_api_template.domain.entities.person_create import PersonCreate
from web_api_template.domain.repository import PersonWriteRepository
from web_api_template.infrastructure.models.dynamodb import PersonModel


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

        my_dump = entity.model_dump(exclude_none=True, exclude_defaults=True)
        entity_model: PersonModel = PersonModel(**my_dump)

        try:
            entity_model.save()
            return mapper.map(entity_model, Person)
        except Exception as ex:
            logger.exception("Saving error")
            raise ex

    async def __get_by_id(self, id: str) -> PersonModel | None:
        """Get person model by ID

        Args:
            id (str): _description_

        Returns:
            PersonModel: _description_
        """

        try:
            entity_model: PersonModel = PersonModel.get(id)

            if not entity_model:
                logger.debug("Item with id: {} not found", id)
                raise ItemNotFoundException(f"Item with id: {id} not found")

            return entity_model

        except PersonModel.DoesNotExist as nex:
            logger.exception("Item does not exists")
            raise ItemNotFoundException(f"Item with id: {id} not found")

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
        try:
            PersonModel.get(id).delete()

        except PersonModel.DoesNotExist as nex:
            logger.exception("Item does not exists")
            raise ItemNotFoundException(f"Item with id: {id} not found")
        except Exception as ex:
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
                # TODO : check if item is in delete status
                logger.debug("Item with id: {} not found", id)
                raise ItemNotFoundException(f"Item with id: {id} not found")

            # Delete the given (and existing) id
            await self.__delete(id)

        except Exception as ex:
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
            # TODO: careful, we need a model to update and not update fields as id
            entity_model: Optional[PersonModel] = await self.__get_by_id(id)

            if not entity_model:
                # TODO : check if person is in delete status
                logger.debug("Item with id: {} not found", id)
                raise ItemNotFoundException(f"Item with id: {id} not found")

            # TODO: check for unique slug

            my_dump = person.model_dump(exclude_none=True)
            new_model: PersonModel = PersonModel(**my_dump)
            # Always set id. If not, a new object with a different id will be created
            new_model.id = id

            new_model.save()
            new_model.refresh()

            return mapper.map(new_model, Person)

        except Exception as ex:
            logger.exception("Database error")
            raise ex
