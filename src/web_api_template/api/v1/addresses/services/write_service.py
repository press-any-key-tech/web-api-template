from typing import Optional

from pydilite import inject

from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.domain.exceptions import (
    AddressNotFoundException,
    PersonNotFoundException,
)
from web_api_template.domain.repository import AddressWriteRepository
from web_api_template.domain.value_objects import Address, AddressCreate


class WriteService:
    """Command operations"""

    @inject()
    def __init__(self, address_db_repo: AddressWriteRepository):
        self.address_db_repo = address_db_repo

    async def create(
        self,
        # current_user: User,
        person_id: str,
        request: AddressCreate,
    ) -> Optional[Address]:
        """
        Create an address associated to a person

        Args:
            current_user (User): The current user creating the address.
            person_id (str): The person ID to associate the address with.
            request (Address): The requested address to create.

        Returns:
            Address: The newly created address in the response format.
        """

        logger.debug("Entering. Address: {}", request)

        # if not await can_create(current_user=current_user):
        #     raise NotAllowedCreationException(
        #         "You are not allowed to create this item"
        #     )

        try:

            response: Optional[Address] = await self.address_db_repo.create(
                # current_user=current_user,
                person_id=person_id,
                entity=request,
            )

            return response

        except ItemNotFoundException:
            # Domain exception raise if template does not exists
            raise PersonNotFoundException(id=person_id)

    async def delete_by_person_and_id(self, person_id: str, id: str):
        """
        Delete the Address object with the given ID

        Args:
            id (UUID): ID of the content to be deleted
            current_user (User): User object who is performing the deletion

        Raises:
            ContentModificationNotAllowedException: If the current user is not allowed to modify the given content
            ContentNotFoundException: If the content with the given ID is not found in the database

        Returns:
            None
        """

        # TODO: check if person and address id exists?

        logger.debug("Entering. id: {}", id)

        try:
            await self.address_db_repo.delete_by_person(person_id=person_id, id=id)

        except ItemNotFoundException:
            # Domain exception raise if content doesn't exists
            raise AddressNotFoundException(f"Address with id [{id}] not found")

    # async def update(
    #     self,
    #     id: str,
    #     request: Content,
    #     # current_user: User
    # ) -> Optional[Content]:
    #     """
    #     Updates the given content

    #     Args:
    #         id (UUID): Content ID
    #         content_request (Content): New values for the Content

    #     Returns:
    #         Content: domain entity to return
    #     """

    #     logger.debug("Entering. id: {} request: {}", id, request)

    #     try:
    #         result: Optional[Content] = await self.content_db_repo.update(
    #             id=id, content=request
    #         )

    #         return result

    #     except ItemNotFoundException:
    #         # Domain exception raise if template does not exists
    #         raise ContentNotFoundException(f"Content with id [{id}] not found")
