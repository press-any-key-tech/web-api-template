from typing import TYPE_CHECKING, List

from ksuid import Ksuid
from web_api_template.core.repository.model.sqlalchemy import Base, BaseModel

from sqlalchemy import Column, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .address_model import AddressModel

# from .policy_model import PolicyModel


class PersonModel(BaseModel, Base):
    """Repository persons model

    Args:
        Base (_type_): SQLAlchemy base model
        BaseModel (_type_): base entity model
    """

    __tablename__ = "persons"

    id: Mapped[str] = mapped_column(
        String(27),
        primary_key=True,
        default=lambda: str(Ksuid()),
        index=True,
    )

    name: Mapped[str] = mapped_column(String(500), nullable=False)
    surname: Mapped[str] = mapped_column(String(500), nullable=False)
    email: Mapped[str] = mapped_column(String(500), nullable=False)
    identification_number: Mapped[str] = mapped_column(
        String(500), nullable=False, unique=True
    )

    addresses: Mapped[List["AddressModel"]] = relationship(
        "AddressModel", back_populates="person"
    )

    policies: Mapped[List["PolicyModel"]] = relationship(
        "PolicyModel", back_populates="policy_holder"
    )
