
from ksuid import Ksuid
from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex

from web_api_template.core.repository.attributes.dynamodb import EnumAttribute
from web_api_template.core.repository.model.dynamodb import BaseModel
from web_api_template.domain.types import PolicyStatusEnum


class PersonIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """

    class Meta:
        # index_name is optional, but can be provided to override the default name
        index_name = "policy-person-index"
        read_capacity_units = 2
        write_capacity_units = 1
        # All attributes are projected
        projection = AllProjection()

    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    person_id = UnicodeAttribute(default="", hash_key=True)


class PolicyModel(BaseModel):
    """
    A DynamoDB Policy
    """

    class Meta(BaseModel.Meta):
        table_name = "policies"

    id: str = UnicodeAttribute(hash_key=True, default=lambda: str(Ksuid()), null=False)

    person_index = PersonIndex()
    person_id: str = UnicodeAttribute(null=False)

    policy_number: str = UnicodeAttribute(null=False)

    status: str = EnumAttribute(enum_type=PolicyStatusEnum, null=True)
