from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from web_api_template.domain.entities.person_base import PersonBase
from web_api_template.domain.value_objects import Address


class PersonCreate(PersonBase):
    """
    Represents a data structure to create a person.

    """

    ...

    # address_ids: Optional[List[str]] = Field(
    #     default=[],
    #     json_schema_extra={
    #         "description": "List of address IDs to associate to this person."
    #     },
    # )
