from typing import Any, List, Tuple

from fastapi import Depends, HTTPException, Request, status

from web_api_template.core.auth.group_checker import GroupChecker
from web_api_template.core.logging import logger


def require_groups(allowed_groups: List[str]):
    """Check if the user has the required groups

    Args:
        allowed_groups (List[str]): _description_
    """

    def _group_checker(request: Request):
        return GroupChecker(allowed_groups)(request)

    return _group_checker
