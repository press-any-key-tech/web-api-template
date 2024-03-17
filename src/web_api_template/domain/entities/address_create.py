from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from web_api_template.domain.entities.address_base import AddressBase


class AddressCreate(AddressBase):
    """
    Represents a data structure to create a address.

    Why a list of ids instead of a list of objects?
    To avoid circular dependencies and to avoid creating a new object when creating a address.

    """

    ...
