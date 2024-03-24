from typing import Optional

from pynamodb.models import Model

from .settings import settings


class BaseModel(Model):
    """
    A DynamoDB Base Model
    """

    class Meta:
        table_name: Optional[str] = None
        region: str = settings.DYNAMODB_REGION
        if settings.DYNAMODB_ENDPOINT is not None:
            host: str = settings.DYNAMODB_ENDPOINT
