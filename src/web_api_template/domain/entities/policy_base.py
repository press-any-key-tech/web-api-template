from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, validator

from web_api_template.domain.types import PolicyStatusEnum

from web_api_template.core.domain.validators import ksuid_validator


class PolicyBase(BaseModel):
    """
    Represents a data structure for an insurance policy.
    """

    id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique Policy ID (ksuid)",
            "example": "0ujsswThIGTUYm2K8FjOOfXtY1K",
        },
    )

    policy_number: str = Field(
        ...,
        max_length=150,
        json_schema_extra={
            "description": "Policy unique number",
            "example": "AB-111-333-555",
        },
    )

    status: PolicyStatusEnum = Field(
        default=PolicyStatusEnum.INACTIVE,
        json_schema_extra={
            "description": "Policy status",
            "example": "inactive",
        },
    )

    @field_validator("id")
    def validate_ksuid(cls, value, values, **kwargs):
        return ksuid_validator(value)
