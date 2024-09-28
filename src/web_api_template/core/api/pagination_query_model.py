from typing import Optional

from pydantic import BaseModel, Field

from .sorting_query_model import SortingQueryModel


class PaginationQueryModel(SortingQueryModel):
    """Provides the interface for pagination and sorting."""

    page: Optional[int] = Field(
        default=1,
        ge=1,
        json_schema_extra={"description": "Page number", "example": "1"},
    )
    size: Optional[int] = Field(
        default=10,
        ge=1,
        json_schema_extra={"description": "Page Size", "example": "10"},
    )

    class Config:
        extra = "forbid"
