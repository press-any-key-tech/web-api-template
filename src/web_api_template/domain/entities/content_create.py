from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from web_api_template.domain.entities import Address
from web_api_template.domain.entities.content_base import ContentBase
from web_api_template.domain.entities.policy import Policy


class ContentCreate(ContentBase):
    """
    Represents a data structure to create a content.

    Why a list of ids instead of a list of objects?
    To avoid circular dependencies and to avoid creating a new object when creating a content.

    """

    ...
