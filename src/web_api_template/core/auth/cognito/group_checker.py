from typing import List

from fastapi import Depends, HTTPException

from web_api_template.core.logging import logger

from .settings import settings
from .user import User
from .utils import get_current_active_user


class GroupChecker:
    """Controls if user has the required group (user_type)"""

    __allowed_groups: list = []

    def __init__(self, allowed_groups: List):
        self.__allowed_groups = allowed_groups

    def __call__(self, user: User = Depends(get_current_active_user)):
        if settings.AUTH_DISABLED:
            return

        if not any(group in self.__allowed_groups for group in user.groups):
            logger.debug(
                f"User with groups {user.groups} not in {self.__allowed_groups}"
            )
            raise HTTPException(status_code=403, detail="Operation not allowed")
