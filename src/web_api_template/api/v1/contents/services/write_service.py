from typing import Optional

from pydilite import inject

from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.domain.entities import Content, ContentFilter
from web_api_template.domain.entities.content_create import ContentCreate
from web_api_template.domain.exceptions import ContentNotFoundException
from web_api_template.domain.repository import ContentWriteRepository


class WriteService:
    """Command operations"""

    @inject()
    def __init__(self, content_db_repo: ContentWriteRepository):
        self.content_db_repo = content_db_repo

    async def create(
        self,
        # current_user: User,
        request: ContentCreate,
    ) -> Optional[Content]:
        """
        Create a Content.

        Args:
            current_user (User): The current user creating the content.
            request (Content): The requested content to create.

        Returns:
            Content: The newly created content in the response format.
        """

        logger.debug("Entering. content: %s", request)

        # if not await can_create(current_user=current_user):
        #     raise NotAllowedCreationException(
        #         "You are not allowed to create this item"
        #     )

        response: Optional[Content] = await self.content_db_repo.create(
            # current_user=current_user,
            entity=request
        )

        return response

    async def delete_by_id(self, id: str):
        """
        Delete the Content object with the given ID

        Args:
            id (UUID): ID of the content to be deleted
            current_user (User): User object who is performing the deletion

        Raises:
            ContentModificationNotAllowedException: If the current user is not allowed to modify the given content
            ContentNotFoundException: If the content with the given ID is not found in the database

        Returns:
            None
        """

        logger.debug("Entering. id: %s", id)

        try:
            await self.content_db_repo.delete(id=id)

        except ItemNotFoundException:
            # Domain exception raise if content doesn't exists
            raise ContentNotFoundException(f"Content with id [{id}] not found")

    async def update(
        self,
        id: str,
        request: Content,
        # current_user: User
    ) -> Optional[Content]:
        """
        Updates the given content

        Args:
            id (UUID): Content ID
            content_request (Content): New values for the Content

        Returns:
            Content: domain entity to return
        """

        logger.debug("Entering. id: %s request: %s", id, request)

        try:
            result: Optional[Content] = await self.content_db_repo.update(
                id=id, content=request
            )

            return result

        except ItemNotFoundException:
            # Domain exception raise if template does not exists
            raise ContentNotFoundException(f"Content with id [{id}] not found")
