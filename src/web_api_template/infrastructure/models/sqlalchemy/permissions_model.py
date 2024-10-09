from typing import ForwardRef, List

from ksuid import Ksuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from web_api_template.core.repository.model.sqlalchemy import Base, BaseModel


class PermissionsModel(BaseModel, Base):
    """User permissions model

    Args:
        Base (_type_): SQLAlchemy base model
        BaseModel (_type_): base entity model
    """

    __tablename__ = "permissions"

    id: Mapped[str] = mapped_column(
        String(27),
        primary_key=True,
        default=lambda: str(Ksuid()),
        index=True,
    )

    username: Mapped[str] = mapped_column(String(500), nullable=False)
    permission: Mapped[str] = mapped_column(String(500), nullable=False)
