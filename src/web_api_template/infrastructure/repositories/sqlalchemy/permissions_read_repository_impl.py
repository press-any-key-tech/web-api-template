from typing import List, Optional

from automapper import mapper
from sqlalchemy import select

from web_api_template.core.api.pagination_query_model import PaginationQueryModel
from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.core.repository.manager.sqlalchemy.async_database import (
    AsyncDatabase,
)
from web_api_template.core.repository.manager.sqlalchemy.async_paginator import (
    AsyncPaginator,
)
from web_api_template.core.repository.manager.sqlalchemy.page import Page
from web_api_template.domain.repository.permissions_read_repository import (
    PermissionsReadRepository,
)
from web_api_template.infrastructure.models.sqlalchemy.permissions_model import (
    PermissionsModel,
)


class PermissionsReadRepositoryImpl(PermissionsReadRepository):
    """Repository implementation for Permissions"""

    async def get_permissions_by_username(
        self,
        *,
        username: str,
        # query: CommonQueryModel,
        # current_user: User,
    ) -> List[str]:
        """Gets filtered policies

        Args:
            request (Request): request (from fastAPI)
            current_user (AuthUser, optional): Current user who makes the request
            username: username of the person
            query: parameter in pagination(page, size, sort)

        Returns:
            dict
        """

        logger.debug("User name: {}", username)
        # logger.debug("query: %s", query)

        async with AsyncDatabase.get_session(self._label) as session:
            try:

                result = await session.execute(
                    select(PermissionsModel).where(
                        PermissionsModel.username == username
                    )
                )
                # It is done this way while I am creating the unit tests
                scalars = result.scalars()
                items = scalars.all()
                return [item.permission for item in items]

            except Exception as ex:
                logger.exception("AsyncDatabase error")
                raise ex
