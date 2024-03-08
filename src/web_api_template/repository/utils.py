"""Utility methods for repository operation
"""

from datetime import datetime
from typing import Any, overload

from web_api_template.core.auth.user import User
from web_api_template.core.repository.postgresql import BaseModel


@overload
def set_concurrency_fields(source: BaseModel, real_user: User) -> None: ...


@overload
def set_concurrency_fields(source: BaseModel, user_id: str) -> None: ...


def set_concurrency_fields(source: BaseModel, user: Any) -> None:
    """Alternate version of 'set_concurrency_fields_full_detail' that allows to NOT specify the datetime when the operation is performed.
    'now' is assumed.
    """
    set_concurrency_fields_full_detail(
        source=source, user=user, the_instant=datetime.utcnow()
    )


def set_concurrency_fields_full_detail(
    source: BaseModel, user: Any, the_instant: datetime
) -> None:
    """Modifies concurrency (audit?) fields (creation and modification date and user)

    Args:
        source (BaseModel): Base model with concurrency fields
        user (Any): Has valid behavior for "str" and "User" types
        the_instant (datetime): timestamp for the operation
    """

    if user is None:
        raise AttributeError("'User' may not be None!")

    effective_user_id = None

    if isinstance(user, User):
        effective_user_id = user.id

    if isinstance(user, str):
        effective_user_id = user

    if effective_user_id is None:
        raise AttributeError("'User' not of valid class!")

    # Check if source has attributes, if not, ignore
    if not hasattr(source, "created_at") or not hasattr(source, "updated_at"):
        return

    # Set attributes
    if not source.created_at or not source.created_by:
        # Multiple assignation ;-)
        source.created_at = source.updated_at = the_instant
        source.created_by = source.updated_by = effective_user_id
    else:
        source.updated_at = the_instant
        source.updated_by = effective_user_id
