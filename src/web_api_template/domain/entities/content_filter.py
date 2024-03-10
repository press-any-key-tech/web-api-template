from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from web_api_template.domain.types.currency_enum import CurrencyEnum


class ContentFilter(BaseModel):
    """
    Represents a data structure for filtering contents.

    Args:
        BaseModel (BaseModel): Inherited properties.
    """

    id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique Content ID (ksuid)",
            "example": "0ujsswThIGTUYm2K8FjOOfXtY1K",
        },
    )

    name: Optional[str] = Field(
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

    value: Optional[float] = Field(
        ...,
        json_schema_extra={
            "description": "Content value",
            "example": "12345678",
        },
    )

    value_currency: Optional[CurrencyEnum] = Field(
        default=...,
        json_schema_extra={
            "description": "Content value currency",
            "example": "EUR",
        },
    )
