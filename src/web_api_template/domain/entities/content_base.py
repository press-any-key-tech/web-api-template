from typing import Optional

from pydantic import BaseModel, Field, field_validator

from web_api_template.core.domain.validators import ksuid_validator
from web_api_template.domain.types import CurrencyEnum


class ContentBase(BaseModel):
    """
    Represents a data structure for a policy content.
    """

    id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique Content ID (ksuid)",
            "example": "0ujsswThIGTUYm2K8FjOOfXtY1K",
        },
    )

    name: str = Field(
        default=None,
        max_length=500,
        json_schema_extra={
            "description": "Content name",
            "example": "Steinway & Sons Grand Piano (1989 model)",
        },
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500,
        json_schema_extra={
            "description": "Content description",
            "example": "Dinner room piano",
        },
    )

    value: float = Field(
        ...,
        json_schema_extra={
            "description": "Content value",
            "example": "12345678",
        },
    )

    value_currency: CurrencyEnum = Field(
        default=...,
        json_schema_extra={
            "description": "Content value currency",
            "example": "EUR",
        },
    )

    @field_validator("id")
    def validate_ksuid(cls, value, values, **kwargs):
        return ksuid_validator(value)
