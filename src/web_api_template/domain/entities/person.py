

from web_api_template.domain.entities.person_base import PersonBase


class Person(PersonBase):
    """
    Represents a data structure for a person when retrieving data.
    """

    # addresses: Optional[List[Address]] = Field(
    #     default=[],
    #     json_schema_extra={"description": "Person addresses"},
    # )

    ...
