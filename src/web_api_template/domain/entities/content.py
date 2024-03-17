from typing import Optional

from pydantic import BaseModel, Field, field_validator

from web_api_template.core.domain.validators import ksuid_validator
from web_api_template.domain.entities.content_base import ContentBase
from web_api_template.domain.types import CurrencyEnum


class Content(ContentBase):
    """
    Represents a data structure for a policy content.
    """

    ...
