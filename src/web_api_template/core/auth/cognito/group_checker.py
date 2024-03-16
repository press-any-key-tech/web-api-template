from typing import List

from fastapi import Depends, HTTPException, Request

from web_api_template.core.logging import logger

from .settings import settings
from .user import User


class GroupChecker:
    """Controls if user has the required group (user_type)"""

    __allowed_groups: list = []

    def __init__(self, allowed_groups: List):
        self.__allowed_groups = allowed_groups

    def __call__(self, request: Request):

        if settings.AUTH_DISABLED:
            return

        if not hasattr(request.state, "current_user"):
            raise HTTPException(status_code=401, detail="Authentication required")

        user: User = request.state.current_user

        if not any(group in self.__allowed_groups for group in user.groups):
            logger.debug(
                f"User with groups {user.groups} not in {self.__allowed_groups}"
            )
            raise HTTPException(status_code=403, detail="Operation not allowed")
