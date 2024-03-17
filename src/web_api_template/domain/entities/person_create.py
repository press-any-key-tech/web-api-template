from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from web_api_template.domain.entities import Address
from web_api_template.domain.entities.person_base import PersonBase
from web_api_template.domain.entities.policy import Policy



class PersonCreate(PersonBase):
    """
    Represents a data structure to create a person.

    Why a list of ids instead of a list of objects?
    To avoid circular dependencies and to avoid creating a new object when creating a person.

    """

    address_ids: Optional[List[str]] = Field(
        default=[],
        json_schema_extra={
            "description": "List of address IDs to associate to this person."
        },
    )

    policy_ids: Optional[List[str]] = Field(
        default=[],
        json_schema_extra={
            "description": "List of policy IDs to associate to this person."
        },
    )
