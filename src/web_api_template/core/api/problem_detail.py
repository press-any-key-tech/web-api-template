from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_validator

from .validation_error_detail import ValidationErrorDetail

status_to_section: Dict[int, str] = {
    100: "6.2.1",
    101: "6.2.2",
    200: "6.3.1",
    201: "6.3.2",
    202: "6.3.3",
    203: "6.3.4",
    204: "6.3.5",
    205: "6.3.6",
    206: "https://datatracker.ietf.org/doc/html/rfc7233#section-4.1",
    300: "6.4.1",
    301: "6.4.2",
    302: "6.4.3",
    303: "6.4.4",
    304: "https://datatracker.ietf.org/doc/html/rfc7232#section-4.1",
    305: "6.4.5",
    307: "6.4.7",
    400: "6.5.1",
    401: "https://datatracker.ietf.org/doc/html/rfc7235#section-3.1",
    402: "6.5.2",
    403: "6.5.3",
    404: "6.5.4",
    405: "6.5.5",
    406: "6.5.6",
    407: "https://datatracker.ietf.org/doc/html/rfc7235#section-3.2",
    408: "6.5.7",
    409: "6.5.8",
    410: "6.5.9",
    411: "6.5.10",
    412: "https://datatracker.ietf.org/doc/html/rfc7232#section-4.2",
    413: "6.5.11",
    414: "6.5.12",
    415: "6.5.13",
    416: "https://datatracker.ietf.org/doc/html/rfc7233#section-4.4",
    417: "6.5.14",
    426: "6.5.15",
    500: "6.6.1",
    501: "6.6.2",
    502: "6.6.3",
    503: "6.6.4",
    504: "6.6.5",
    505: "6.6.6",
    # Additional status codes from other RFCs
    422: "https://datatracker.ietf.org/doc/html/rfc4918#section-11.2",
    428: "https://datatracker.ietf.org/doc/html/rfc6585#section-3",
    429: "https://datatracker.ietf.org/doc/html/rfc6585#section-4",
    431: "https://datatracker.ietf.org/doc/html/rfc6585#section-5",
    451: "https://datatracker.ietf.org/doc/html/rfc7725#section-3",
}


# TODO: send to utils
def get_rfc_section_url(status: int) -> str:
    """Get the RFC section URL for a given HTTP status code.

    Args:
        status (int): The HTTP status code.

    Returns:
        str: The URL to the corresponding section in the RFC.
    """
    base_url = "https://datatracker.ietf.org/doc/html/rfc7231#section-"
    section = status_to_section.get(status)
    if section is None:
        return f"{base_url}6.6.1"  # Default to 500 Internal Server Error section
    if section.startswith("https://"):
        return section
    return f"{base_url}{section}"


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

    errors: Optional[List[ValidationErrorDetail]] = Field(
        default=None,
        json_schema_extra={
            "description": "Validation errors",
            "example": [
                {
                    "type": "value_error",
                    "loc": ["body", "id"],
                    "msg": "Value error, Invalid KSUID format",
                    "input": "1234",
                    "ctx": {"error": "Invalid KSUID format"},
                    "url": "https://errors.pydantic.dev/2.9/v/value_error",
                }
            ],
        },
    )

    def add_extension(self, key: str, value: Any) -> None:
        """Add an extension to the ProblemDetail object.

        Args:
            key (str): The key for the extension.
            value (Any): The value for the extension.
        """
        self.__setattr__(key, value)

    @model_validator(mode="before")
    def set_default_type(cls, values):
        """Set the default type based on the status if type is not provided."""
        if "type" not in values or values["type"] is None:
            status = values.get("status", 500)
            values["type"] = get_rfc_section_url(status)
        return values

    class Config:
        extra = "allow"
