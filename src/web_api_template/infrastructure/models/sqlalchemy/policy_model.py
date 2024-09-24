from datetime import date
from typing import cast

from ksuid import Ksuid
from sqlalchemy import Column, Date, Enum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Enum as SQLAEnum

from web_api_template.core.repository.model.sqlalchemy import Base, BaseModel
from web_api_template.domain.types.policy_status_enum import PolicyStatusEnum
from web_api_template.domain.types.policy_type_enum import PolicyTypeEnum

from .person_model import PersonModel


class PolicyModel(Base, BaseModel):
    """Repository policies model

    Args:
        Base (_type_): SQLAlchemy base model
        BaseModel (_type_): base entity model
    """

    __tablename__ = "policies"

    id: Mapped[str] = mapped_column(
        String(27),
        primary_key=True,
        default=lambda: str(Ksuid()),
        index=True,
    )

    # person_id: Mapped[str] = mapped_column(
    #     String(27), ForeignKey("persons.id"), nullable=False
    # )

    # person = relationship("PersonModel", back_populates="policies")

    holder_id: Mapped[str] = mapped_column(
        String(27), ForeignKey("persons.id"), nullable=False
    )

    holder: Mapped["PersonModel"] = relationship(
        "PersonModel", back_populates="policies"
    )

    policy_number: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[Column[SQLAEnum]] = mapped_column(
        Enum(PolicyStatusEnum), nullable=False, default=PolicyStatusEnum.INACTIVE
    )

    policy_type: Mapped[Column[SQLAEnum]] = mapped_column(
        Enum(PolicyTypeEnum), nullable=False
    )

    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    premium: Mapped[float] = mapped_column(Float, nullable=False)
