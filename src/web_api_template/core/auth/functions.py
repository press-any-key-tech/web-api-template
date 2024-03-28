from typing import Any, List, Tuple

from fastapi import Depends, HTTPException, Request, status

from web_api_template.core.auth.group_checker import GroupChecker
from web_api_template.core.logging import logger

from .settings import settings


def require_groups(allowed_groups: List[str]):
    """Check if the user has the required groups

    Args:
        allowed_groups (List[str]): _description_
    """

    def _group_checker(request: Request):
        return GroupChecker(allowed_groups)(request)

    return _group_checker


def require_user():
    """Check if the user is authenticated"""

    def _user_checker(request: Request):

        if settings.AUTH_DISABLED:
            return

        if not hasattr(request.state, "current_user") or not request.state.current_user:
            raise HTTPException(status_code=401, detail="Authentication required")

    return _user_checker
