from typing import Optional

from pydantic import BaseModel, Field


class SortingQueryModel(BaseModel):
    """Provides the interface for sorting."""

    sort: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Sort fields separated by comma",
            "example": "-id,key",
        },
    )
