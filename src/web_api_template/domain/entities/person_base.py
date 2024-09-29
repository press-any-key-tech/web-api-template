from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from web_api_template.core.domain.validators import ksuid_validator


class PersonBase(BaseModel):
    """
    Represents a data structure for a person.
    """

    id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique Person ID (ksuid)",
            "example": "0ujsswThIGTUYm2K8FjOOfXtY1K",
        },
    )

    name: str = Field(
        ...,
        max_length=500,
        json_schema_extra={
            "description": "Person name",
            "example": "John",
        },
    )

    surname: str = Field(
        ...,
        max_length=500,
        json_schema_extra={
            "description": "Person surname/s",
            "example": "Doe",
        },
    )

    email: EmailStr = Field(
        ...,
        max_length=150,
        json_schema_extra={
            "description": "Person email",
            "example": "johndoe@mail.com",
        },
    )

    identification_number: str = Field(
        ...,
        max_length=50,
        json_schema_extra={
            "description": "Person identification number",
            "example": "123456789",
        },
    )

    @field_validator("id")
    def validate_ksuid(cls, value, values, **kwargs):
        return ksuid_validator(value)
