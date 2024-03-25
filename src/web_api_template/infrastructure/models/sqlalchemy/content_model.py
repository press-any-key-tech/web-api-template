from typing import cast

from ksuid import Ksuid
from sqlalchemy import Column, Enum, Float, ForeignKey, String
from sqlalchemy.sql.sqltypes import Enum as SQLAEnum

from web_api_template.core.repository.model.sqlalchemy import Base, BaseModel
from web_api_template.domain.types.currency_enum import CurrencyEnum


class ContentModel(Base, BaseModel):
    """Repository content model

    Args:
        Base (_type_): SQLAlchemy base model
        BaseModel (_type_): base entity model
    """

    __tablename__ = "contents"

    id = Column(
        String(27),
        primary_key=True,
        default=lambda: str(Ksuid()),
        index=True,
    )

    policy_id = Column(String, ForeignKey("policies.id"), nullable=False)

    name = Column(String(500), nullable=False)
    description = Column(String(500), nullable=True)
    value = Column(Float, nullable=False, default=0.0)

    value_currency: Column[SQLAEnum] = Column(
        Enum(CurrencyEnum), nullable=False, default=CurrencyEnum.EUR
    )
