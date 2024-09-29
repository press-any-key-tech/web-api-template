

from web_api_template.domain.aggregates import PolicyBase


class PolicyCreate(PolicyBase):
    """
    Represents a data structure to create a policy.

    Why a list of ids instead of a list of objects?
    To avoid circular dependencies and to avoid creating a new object when creating a person.

    """

    ...

    # contents_ids: Optional[List[str]] = Field(
    #     default=[],
    #     json_schema_extra={
    #         "description": "List of contents IDs to associate to this policy."
    #     },
    # )

    # building_id: Optional[str] = Field(
    #     default=[],
    #     json_schema_extra={"description": "Building to associate to this policy."},
    # )
