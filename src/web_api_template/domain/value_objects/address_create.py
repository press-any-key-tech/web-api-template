from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from web_api_template.domain.value_objects.address_base import AddressBase


class AddressCreate(AddressBase):
    """
    Represents a data structure to create an address.

    """

    ...
