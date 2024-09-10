import uuid

from ksuid import Ksuid
from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from pynamodb.models import Model

from web_api_template.core.repository.model.dynamodb import BaseModel


class EmailIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """

    class Meta:
        # index_name is optional, but can be provided to override the default name
        index_name = "person-email-index"
        read_capacity_units = 2
        write_capacity_units = 1
        # All attributes are projected
        projection = AllProjection()

    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    email: str = UnicodeAttribute(default="", hash_key=True)


class PersonModel(BaseModel):
    """
    A DynamoDB Person Model
    """

    class Meta(BaseModel.Meta):
        table_name = "persons"

    id: str = UnicodeAttribute(hash_key=True, default=lambda: str(Ksuid()), null=False)
    name: str = UnicodeAttribute()
    surname: str = UnicodeAttribute()

    email_index = EmailIndex()
    email: str = UnicodeAttribute()
