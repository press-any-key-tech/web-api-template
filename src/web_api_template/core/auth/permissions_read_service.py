from typing import List, Optional

from pydilite import inject

from web_api_template.core.logging import logger
from web_api_template.core.repository.manager.sqlalchemy.page import Page
from web_api_template.domain.repository.permissions_read_repository import (
    PermissionsReadRepository,
)


class PermissionsReadService:
    """Query operations"""

    @inject()
    def __init__(self, permissions_db_repo: PermissionsReadRepository):
        self.permissions_db_repo = permissions_db_repo

    async def get_permissions(self, username: str) -> List[str]:
        """
        Get a list of persons

        Args:
            filter (PersonFilter): Person related filter

        Returns:
            List[Person]: domain entity to return
        """

        logger.debug("Entering. username: {}", username)

        result: List[str] = await self.permissions_db_repo.get_permissions_by_username(
            username=username
        )

        return result
