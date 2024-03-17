from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class PersonFilter(BaseModel):
    """
    Represents a data structure for filtering persons.

    Args:
        BaseModel (BaseModel): Inherited properties.
    """

    id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique Person ID (ksuid)",
            "example": "0ujsswThIGTUYm2K8FjOOfXtY1K",
        },
    )

    name: Optional[str] = Field(
        default=None,
        max_length=500,
        json_schema_extra={
            "description": "Person name",
            "example": "John",
        },
    )

    surname: Optional[str] = Field(
        default=None,
        max_length=500,
        json_schema_extra={
            "description": "Person surname/s",
            "example": "Doe",
        },
    )

    email: Optional[EmailStr] = Field(
        default=None,
        max_length=150,
        json_schema_extra={
            "description": "Person email",
            "example": "johndoe@mail.com",
        },
    )
