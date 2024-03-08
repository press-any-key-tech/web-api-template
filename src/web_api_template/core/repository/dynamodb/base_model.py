from pynamodb.models import Model

from web_api_template.core.settings import settings


class BaseModel(Model):
    """
    A DynamoDB Base Model
    """

    class Meta:
        table_name = None
        region = settings.DYNAMODB_REGION
        if settings.DYNAMODB_ENDPOINT is not None:
            host = settings.DYNAMODB_ENDPOINT
