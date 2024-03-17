from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, root_validator


class User(BaseModel):
    """Application User

    Args:
        BaseModel (BaseModel): Inherited properties
    """

    id: str = Field(
        ...,
        max_length=500,
        json_schema_extra={
            "description": "Unique user ID (sub)",
            "example": "0ujsswThIGTUYm2K8FjOOfXtY1K",
        },
    )
    name: Optional[str] = Field(
        default=None,
        max_length=500,
        json_schema_extra={
            "description": "User name",
            "example": "test_user",
        },
    )
    email: Optional[EmailStr] = Field(
        default=None,
        max_length=500,
        json_schema_extra={
            "description": "User's email address (Optional)",
            "example": "useradmin@user.com",
        },
    )
    groups: Optional[List[str]] = Field(
        default=[],
        json_schema_extra={
            "description": "List of user groups",
            "example": '["admin", "user"]',
        },
    )
