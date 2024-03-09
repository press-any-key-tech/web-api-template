from typing import Optional

from pydantic import BaseModel, Field, field_validator

from web_api_template.core.domain.validators import ksuid_validator
from web_api_template.domain.entities import Address
from web_api_template.domain.entities.building_base import BuildingBase
from web_api_template.domain.types import CurrencyEnum


class Building(BuildingBase):
    """
    Represents a data structure for a policy building.
    """

    ...
