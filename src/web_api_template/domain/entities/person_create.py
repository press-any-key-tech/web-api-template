

from web_api_template.domain.entities.person_base import PersonBase


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
