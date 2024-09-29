from typing import Any, List, Optional

from pydantic import BaseModel, Field


class Page(BaseModel):
    """Database page model for async queries

    Args:
        BaseModel (_type_): _description_
    """

    page: Optional[int] = Field(
        default=1,
        ge=1,
        json_schema_extra={"description": "Page number", "example": "1"},
    )
    pages: Optional[int] = Field(
        default=1,
        ge=1,
        json_schema_extra={"description": "Total pages", "example": "100"},
    )
    total: Optional[int] = Field(
        default=0,
        ge=0,
        json_schema_extra={"description": "Total items", "example": "1000"},
    )
    size: Optional[int] = Field(
        default=10,
        ge=1,
        json_schema_extra={"description": "Page Size", "example": "10"},
    )

    items: Optional[List[Any]] = Field(
        default=[],
        json_schema_extra={"description": "Items in the page", "example": "[]"},
    )

    class Config:
        extra = "forbid"
