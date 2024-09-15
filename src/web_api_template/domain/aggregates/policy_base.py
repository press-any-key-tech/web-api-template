from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from web_api_template.core.domain.validators import ksuid_validator
from web_api_template.domain.entities.person import Person
from web_api_template.domain.types import PolicyStatusEnum, PolicyTypeEnum


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

    policy_type: PolicyTypeEnum = Field(
        ...,
        json_schema_extra={
            "description": "Policy type",
            "example": "car",
        },
    )

    policy_holder: Person = Field(
        ...,
        json_schema_extra={
            "description": "Policy holder",
            "example": "Person object",
        },
    )

    start_date: date = Field(
        ...,
        json_schema_extra={
            "description": "Policy start date",
            "example": "2024/01/01",
        },
    )

    end_date: Optional[date] = Field(
        default=None,
        json_schema_extra={
            "description": "Policy end date",
            "example": "2025/01/01",
        },
    )

    premium: float = Field(
        default=0.0,
        json_schema_extra={
            "description": "Policy total premium",
            "example": "123456",
        },
    )

    # contents: Optional[List[ContentItem]]  # Only for content-based policies

    @field_validator("id")
    def validate_ksuid(cls, value, values, **kwargs):
        return ksuid_validator(value)
