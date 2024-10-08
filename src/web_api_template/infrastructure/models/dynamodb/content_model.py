
from ksuid import Ksuid
from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex

from web_api_template.core.repository.attributes.dynamodb import EnumAttribute
from web_api_template.core.repository.model.dynamodb import BaseModel
from web_api_template.domain.types import CurrencyEnum


class PolicyIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """

    class Meta:
        # index_name is optional, but can be provided to override the default name
        index_name = "content-policy-index"
        read_capacity_units = 2
        write_capacity_units = 1
        # All attributes are projected
        projection = AllProjection()

    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    policy_id = UnicodeAttribute(default="", hash_key=True)


class ContentModel(BaseModel):
    """
    A DynamoDB Policy Content
    """

    class Meta(BaseModel.Meta):
        table_name = "contents"

    id: str = UnicodeAttribute(hash_key=True, default=lambda: str(Ksuid()), null=False)

    policy_index = PolicyIndex()
    policy_id: str = UnicodeAttribute(null=False)

    name: str = UnicodeAttribute(null=False)
    description: str = UnicodeAttribute(null=False)
    value: float = NumberAttribute(null=False)
    value_currency: str = EnumAttribute(
        enum_type=CurrencyEnum, null=False, default=CurrencyEnum.EUR.value
    )
