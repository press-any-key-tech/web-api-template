from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from web_api_template.domain.types import PolicyStatusEnum


class PolicyFilter(BaseModel):
    """
    Represents a data structure for filtering policies.
    TODO: Filter by person_id

    Args:
        BaseModel (BaseModel): Inherited properties.
    """

    id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique Policy ID (ksuid)",
            "example": "0ujsswThIGTUYm2K8FjOOfXtY1K",
        },
    )

    policy_number: Optional[str] = Field(
        default=None,
        max_length=500,
        json_schema_extra={
            "description": "Policy number",
            "example": "1234GFDG1234",
        },
    )

    status: Optional[PolicyStatusEnum] = Field(
        default=None,
        json_schema_extra={
            "description": "Policy status",
            "example": "inactive",
        },
    )
