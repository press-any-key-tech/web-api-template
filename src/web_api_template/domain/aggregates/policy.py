


# from web_api_template.domain.entities import Person

from .policy_base import PolicyBase


class Policy(PolicyBase):
    """
    Represents a data structure for an insurance policy for reading.
    """

    ...

    # insured_persons: Optional[List[Person]] = Field(
    #     default=[],
    #     json_schema_extra={"description": "Insured persons"},
    # )

    # address: Optional[Address] = Field(
    #     default=None,
    #     json_schema_extra={
    #         "description": "Address for the policy. Only for home or car insurance",
    #         "example": "Address object",
    #     },
    # )
