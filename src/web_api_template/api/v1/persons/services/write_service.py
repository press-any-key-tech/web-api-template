from web_api_template.core.di_injector import inject
from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.domain.entities import Person, PersonFilter
from web_api_template.domain.entities.person_create import PersonCreate
from web_api_template.domain.exceptions import PersonNotFoundException
from web_api_template.domain.repository import PersonRepository


class WriteService:
    """Command operations"""

    @inject()
    def __init__(self, person_db_repo: PersonRepository):
        self.person_db_repo = person_db_repo

    async def create(
        self,
        # current_user: User,
        request: PersonCreate,
    ) -> Person:
        """
        Create a Person.

        Args:
            current_user (User): The current user creating the person.
            request (Person): The requested person to create.

        Returns:
            Person: The newly created person in the response format.
        """

        logger.debug("Entering. person: %s", request)

        # if not await can_create(current_user=current_user):
        #     raise NotAllowedCreationException(
        #         "You are not allowed to create this item"
        #     )

        response: Person = await self.person_db_repo.create(
            # current_user=current_user,
            entity=request
        )

        return response

    async def delete_by_id(self, id: str):
        """
        Delete the Person object with the given ID

        Args:
            id (UUID): ID of the person to be deleted
            current_user (User): User object who is performing the deletion

        Raises:
            PersonModificationNotAllowedException: If the current user is not allowed to modify the given person
            PersonNotFoundException: If the person with the given ID is not found in the database

        Returns:
            None
        """

        logger.debug("Entering. id: %s", id)

        try:
            await self.person_db_repo.delete(id=id)

        except ItemNotFoundException:
            # Domain exception raise if person doesn't exists
            raise PersonNotFoundException(f"Person with id [{id}] not found")

    async def update(
        self,
        id: str,
        request: PersonCreate,
        # current_user: User
    ) -> Person:
        """
        Updates the given person

        Args:
            id (UUID): Person ID
            person_request (Person): New values for the Person

        Returns:
            Person: domain entity to return
        """

        logger.debug("Entering. id: %s request: %s", id, request)

        try:
            result: Person = await self.person_db_repo.update(id=id, person=request)

            return result

        except ItemNotFoundException:
            # Domain exception raise if template does not exists
            raise PersonNotFoundException(f"Person with id [{id}] not found")
