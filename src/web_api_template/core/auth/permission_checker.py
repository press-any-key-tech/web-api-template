import asyncio
from typing import List

import nest_asyncio
from auth_middleware.logging import logger
from auth_middleware.settings import settings
from auth_middleware.types import User
from fastapi import HTTPException, Request

from web_api_template.core.auth.permissions_read_service import PermissionsReadService

# Apply patch to allow asyncio.run()
nest_asyncio.apply()


class PermissionChecker:
    """Controls if user has the required permissions"""

    __allowed_permissions: List[str] = []

    def __init__(self, allowed_permissions: List[str]):
        self.__allowed_permissions = allowed_permissions

    async def __call__(self, request: Request):

        if settings.AUTH_MIDDLEWARE_DISABLED:
            return

        if not hasattr(request.state, "current_user") or not request.state.current_user:
            raise HTTPException(status_code=401, detail="Authentication required")

        user: User = request.state.current_user

        # Recover permissions for user looking in redis and database
        user_permissions = await PermissionsReadService().get_permissions(user.name)

        if not any(
            permission in self.__allowed_permissions for permission in user_permissions
        ):
            logger.debug(
                f"User with permissions {user_permissions} not in {self.__allowed_permissions}"
            )
            raise HTTPException(status_code=403, detail="Operation not allowed")

    async def get_user_permissions(self, user: User) -> List[str]:
        """Recover permissions for user looking in redis and database

        Args:
            user (User): User object
        Returns:

            List[str]: List of permissions
        """
        return await PermissionsReadService().get_permissions(user.name)
