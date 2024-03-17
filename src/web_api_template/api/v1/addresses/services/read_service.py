from typing import List

from web_api_template.core.di_injector import inject
from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.domain.entities import Content, ContentFilter
from web_api_template.domain.exceptions import ContentNotFoundException
from web_api_template.domain.repository import ContentReadRepository


class ReadService:
    """Query operations"""

    @inject()
    def __init__(self, content_db_repo: ContentReadRepository):
        self.content_db_repo = content_db_repo

    async def get_list(self, filter: ContentFilter) -> List[Content]:
        """
        Get a list of contents

        Args:
            filter (ContentFilter): Content related filter

        Returns:
            List[Content]: domain entity to return
        """

        logger.debug("Entering. filter: %s", filter)

        entities: List[Content] = await self.content_db_repo.get_list(filter=filter)

        return entities

    async def get_by_id(self, id: str) -> Content:
        """
        Search content by id

        Args:
            id (str): id of the content

        Returns:
            content: domain entity to return
        """

        logger.debug("Entering. id: %s", id)

        try:
            entity: Content | None = await self.content_db_repo.get_by_id(id=id)
        except ItemNotFoundException:
            # Domain exception raise if pot doesn't exists
            raise ContentNotFoundException(f"Content with id [{id}] not found")

        return entity

    async def get_list_by_person_id(self, id: str) -> List[Content]:
        """
        Get a list of contents for a given person

        Args:
            id (str): Person id

        Returns:
            List[Content]: domain entity to return
        """

        logger.debug("Entering. filter: %s", id)

        entities: List[Content] = await self.content_db_repo.get_list_by_person_id(
            id=id
        )

        return entities
