from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from web_api_template.domain.entities import Address
from web_api_template.domain.entities.person_base import PersonBase
from web_api_template.domain.entities.policy import Policy


class Person(PersonBase):
    """
    Represents a data structure for a person when retrieving data.
    """

    addresses: Optional[List[Address]] = Field(
        default=[],
        json_schema_extra={"description": "Person addresses"},
    )

    policies: Optional[List[Policy]] = Field(
        default=[],
        json_schema_extra={"description": "Person policies"},
    )
