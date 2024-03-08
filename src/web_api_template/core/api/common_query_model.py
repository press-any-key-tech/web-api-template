from typing import Optional

from pydantic import BaseModel, Field


class CommonQueryModel(BaseModel):
    """Provides the interface for pagination, sorting and query."""

    # q: Optional[str] = Field(
    #     default=None, json_schema_extra={"description": "Query", "example": "something"}
    # )

    sort: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Sort fields", "example": "-id,key"},
    )
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
