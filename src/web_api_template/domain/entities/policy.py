from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, validator

from web_api_template.core.domain.validators import ksuid_validator
from web_api_template.domain.entities import Building, Content

from .policy_base import PolicyBase


class Policy(PolicyBase):
    """
    Represents a data structure for an insurance policy for reading.
    """

    person_id: str = Field(
        ...,
        json_schema_extra={"description": "Insured person id"},
    )

    building: Optional[Building] = Field(
        default=None,
        json_schema_extra={"description": "Insured Building"},
    )

    contents: Optional[List[Content]] = Field(
        default=[],
        json_schema_extra={"description": "Insured contents"},
    )
