import asyncio
from typing import List

from auth_middleware.settings import settings
from fastapi import HTTPException, Request

from .permission_checker import PermissionChecker


def require_permissions(allowed_permissions: List[str]):
    """Check if the user has the required permissions

    Args:
        allowed_permissions (List[str]): a list of required permissions
    """

    async def _permissions_checker(request: Request):
        """Calls the PermissionChecker class to check if
        the user has the required permissions

        Args:
            request (Request): FastAPI request object

        Returns:
            GroupChecker: group checker object
        """
        return await PermissionChecker(allowed_permissions)(request)

    return _permissions_checker
