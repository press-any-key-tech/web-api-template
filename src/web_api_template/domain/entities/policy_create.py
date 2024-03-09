from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from web_api_template.domain.entities import Address
from web_api_template.domain.entities.policy import Policy
from web_api_template.domain.entities.policy_base import PolicyBase


class PolicyCreate(PolicyBase):
    """
    Represents a data structure to create a policy.

    Why a list of ids instead of a list of objects?
    To avoid circular dependencies and to avoid creating a new object when creating a person.

    """

    person_id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Insured person id",
            "example": "0ujsswThIGTUYm2K8FjOOfXtY1K",
        },
    )

    contents_ids: Optional[List[str]] = Field(
        default=[],
        json_schema_extra={
            "description": "List of contents IDs to associate to this policy."
        },
    )

    building_id: Optional[str] = Field(
        default=[],
        json_schema_extra={"description": "Building to associate to this policy."},
    )
