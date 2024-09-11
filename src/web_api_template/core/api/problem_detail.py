from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class ProblemDetail(BaseModel):
    """Problem Detail response object as defined in RFC 7807.

    Args:
        BaseModel (_type_): _description_
    """

    type: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Error type",
            "example": "https://datatracker.ietf.org/doc/html/rfc7231#section-6.5.4",
        },
    )
    title: str = Field(
        default=None,
        json_schema_extra={
            "description": "Error title",
            "example": "And error occurred",
        },
    )
    status: int = Field(
        default=500,
        json_schema_extra={"description": "Error status", "example": "500"},
    )
    detail: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Error description",
            "example": "Something is wrong with the application",
        },
    )
    instance: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Error title",
            "example": "http://localhost:8000/api/v1/persons/1",
        },
    )

    def add_extension(self, key: str, value: Any) -> None:
        """Add an extension to the ProblemDetail object.

        Args:
            key (str): The key for the extension.
            value (Any): The value for the extension.
        """
        setattr(self, key, value)

    @model_validator(mode="before")
    def set_default_type(cls, values):
        """Set the default type based on the status if type is not provided."""
        if "type" not in values or values["type"] is None:
            status = values.get("status", 500)
            values["type"] = (
                f"https://datatracker.ietf.org/doc/html/rfc7231#section-6.5.{status // 100}"
            )
        return values
