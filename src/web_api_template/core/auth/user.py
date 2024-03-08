from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, root_validator


class User(BaseModel):
    """Application User

    Args:
        BaseModel (BaseModel): Inherited properties
    """

    id: str = Field(
        ...,
        # regex="^[A-Za-z0-9#_-]+$",
        description="Unique user ID (sub)",
        example="8e906d39-dc13-479a-97dc-c2c66f878913",
        max_length=50,
    )
    name: str = Field(
        ...,
        description="Username",
        example="test_user",
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description="User's email address (Optional)",
        example="useradmin@user.com",
    )
    groups: List[str] = Field(
        ...,
        description="List of user groups",
        example='["admin", "user"]',
    )
