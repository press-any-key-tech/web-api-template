from typing import cast

from ksuid import Ksuid
from sqlalchemy import Column, Enum, ForeignKey, String

from web_api_template.core.repository.model.sqlalchemy import Base, BaseModel
from web_api_template.domain.types.policy_status_enum import PolicyStatusEnum


class PolicyModel(Base, BaseModel):
    """Repository policies model

    Args:
        Base (_type_): SQLAlchemy base model
        BaseModel (_type_): base entity model
    """

    __tablename__ = "policies"

    id = Column(
        String(27),
        primary_key=True,
        default=lambda: str(Ksuid()),
        index=True,
    )

    person_id = Column(String, ForeignKey("persons.id"), nullable=False)

    policy_number = Column(String(500), nullable=False)
    status = Column(
        Enum(PolicyStatusEnum), nullable=False, default=PolicyStatusEnum.INACTIVE
    )
