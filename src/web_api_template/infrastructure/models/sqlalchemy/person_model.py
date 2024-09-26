from typing import ForwardRef, List

from ksuid import Ksuid
from sqlalchemy import Column, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from web_api_template.core.repository.model.sqlalchemy import Base, BaseModel

from .address_model import AddressModel

# Use ForwardRef to resolve circular imports
PolicyModel = ForwardRef("PolicyModel")


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

    # addresses: Mapped[List["AddressModel"]] = relationship(
    #     "AddressModel", back_populates="person"
    # )

    # policies: Mapped[List["PolicyModel"]] = relationship(
    #     "PolicyModel", back_populates="holder"
    # )


# Now we can resolve the circular import
from .policy_model import PolicyModel

# Update the annotations
PersonModel.__annotations__["policies"] = List[PolicyModel]
