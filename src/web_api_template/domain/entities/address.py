from typing import Optional

from pydantic import BaseModel, Field, field_validator

from web_api_template.core.domain.validators import ksuid_validator


class Address(BaseModel):
    """
    Represents a data structure for an address.
    """

    id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique Address ID (ksuid)",
            "example": "0ujsswThIGTUYm2K8FjOOfXtY1K",
        },
    )

    street: str = Field(
        ...,
        max_length=250,
        json_schema_extra={
            "description": "Street name",
            "example": "1234 Sesame Street",
        },
    )

    city: str = Field(
        ...,
        max_length=150,
        json_schema_extra={"description": "City name", "example": "Anytown"},
    )

    postal_code: str = Field(
        ...,
        max_length=150,
        json_schema_extra={"description": "Postal code", "example": "12345"},
    )

    province: str = Field(
        ...,
        max_length=150,
        json_schema_extra={
            "description": "Province/State/Department",
            "example": "Anyprovince",
        },
    )

    country: str = Field(
        ...,
        max_length=150,
        json_schema_extra={"description": "Country name", "example": "USA"},
    )

    @field_validator("id")
    def validate_ksuid(cls, value, values, **kwargs):
        return ksuid_validator(value)
