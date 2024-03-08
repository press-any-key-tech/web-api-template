from typing import Optional

from pydantic import BaseModel, Field, field_validator

from web_api_template.domain.entities import Address
from web_api_template.domain.types import CurrencyEnum

from web_api_template.core.domain.validators import ksuid_validator


class Building(BaseModel):
    """
    Represents a data structure for a policy building.
    """

    id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique Building ID (ksuid)",
            "example": "0ujsswThIGTUYm2K8FjOOfXtY1K",
        },
    )

    alias: Optional[str] = Field(
        default=None,
        max_length=500,
        json_schema_extra={
            "description": "Building alias name",
            "example": "Beach house",
        },
    )

    value: float = Field(
        ...,
        json_schema_extra={
            "description": "Building value",
            "example": "12345678",
        },
    )

    value_currency: CurrencyEnum = Field(
        default=...,
        json_schema_extra={
            "description": "Building value currency",
            "example": "EUR",
        },
    )

    address: Address = Field(
        ...,
        json_schema_extra={"description": "Building address"},
    )

    @field_validator("id")
    def validate_ksuid(cls, value, values, **kwargs):
        return ksuid_validator(value)
