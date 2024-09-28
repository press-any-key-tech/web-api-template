from typing import List, Optional

from pydilite import inject

from web_api_template.core.api.pagination_query_model import PaginationQueryModel
from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.core.repository.manager.sqlalchemy.page import Page
from web_api_template.domain.entities.person import Person
from web_api_template.domain.entities.person_create import PersonCreate
from web_api_template.domain.entities.person_filter import PersonFilter
from web_api_template.domain.exceptions import PersonNotFoundException
from web_api_template.domain.repository import PersonReadRepository


class ReadService:
    """Query operations"""

    @inject()
    def __init__(self, person_db_repo: PersonReadRepository):
        self.person_db_repo = person_db_repo

    async def get_list(
        self, filter: PersonFilter, pagination: PaginationQueryModel
    ) -> Page:
        """
        Get a list of persons

        Args:
            filter (PersonFilter): Person related filter

        Returns:
            List[Person]: domain entity to return
        """

        logger.debug("Entering. filter: {}", filter)

        result: Page = await self.person_db_repo.get_paginated_list(
            filter=filter, pagination=pagination
        )

        return result

    async def get_by_id(self, id: str) -> Optional[Person]:
        """
        Search person by id

        Args:
            id (str): id of the person

        Returns:
            person: domain entity to return
        """

        logger.debug("Entering. id: {}", id)

        try:
            entity: Optional[Person] = await self.person_db_repo.get_by_id(id=id)
        except ItemNotFoundException:
            # Domain exception raise if pot doesn't exists
            raise PersonNotFoundException(id=id)

        return entity
