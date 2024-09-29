
from ksuid import Ksuid
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from web_api_template.core.repository.model.sqlalchemy import Base, BaseModel


class AddressModel(Base, BaseModel):
    """Repository address model

    Args:
        Base (_type_): SQLAlchemy base model
        BaseModel (_type_): base entity model
    """

    __tablename__ = "addresses"

    id: Mapped[str] = mapped_column(
        String(27),
        primary_key=True,
        default=lambda: str(Ksuid()),
        index=True,
    )

    # policy_id = mapped_column(String, ForeignKey("policies.id"), nullable=False)

    street: Mapped[str] = mapped_column(String(500), nullable=False)
    city: Mapped[str] = mapped_column(String(500), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(500), nullable=False)
    province: Mapped[str] = mapped_column(String(500), nullable=False)
    country: Mapped[str] = mapped_column(String(500), nullable=False)

    person_id: Mapped[str] = mapped_column(
        String(27), ForeignKey("persons.id"), nullable=False
    )

    # person = relationship("PersonModel", back_populates="addresses")
