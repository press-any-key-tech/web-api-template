from typing import cast

from ksuid import Ksuid
from sqlalchemy import Column, Enum, Float, ForeignKey, String

from web_api_template.core.repository.model.sqlalchemy import Base, BaseModel
from web_api_template.domain.types.currency_enum import CurrencyEnum


class AddressModel(Base, BaseModel):
    """Repository address model

    Args:
        Base (_type_): SQLAlchemy base model
        BaseModel (_type_): base entity model
    """

    __tablename__ = "addresses"

    id = Column(
        String(27),
        primary_key=True,
        default=lambda: str(Ksuid()),
        index=True,
    )

    policy_id = Column(String, ForeignKey("policies.id"), nullable=False)

    street = Column(String(500), nullable=False)
    city = Column(String(500), nullable=False)
    postal_code = Column(String(500), nullable=False)
    province = Column(String(500), nullable=False)
    country = Column(String(500), nullable=False)
