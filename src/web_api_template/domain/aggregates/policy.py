from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from web_api_template.core.domain.validators import ksuid_validator

# from web_api_template.domain.entities import Person
from web_api_template.domain.value_objects import Address

from .policy_base import PolicyBase


class Policy(PolicyBase):
    """
    Represents a data structure for an insurance policy for reading.
    """

    # insured_persons: Optional[List[Person]] = Field(
    #     default=[],
    #     json_schema_extra={"description": "Insured persons"},
    # )

    address: Optional[Address] = Field(
        ...,
        json_schema_extra={
            "description": "Address for the policy. Only for home or car insurance",
            "example": "Address object",
        },
    )
