from typing import Optional

from pydantic import BaseModel, Field, field_validator

from web_api_template.core.domain.validators import ksuid_validator
from web_api_template.domain.value_objects.address_base import AddressBase


class Address(AddressBase):
    """
    Represents a data structure for an address.
    """

    ...
