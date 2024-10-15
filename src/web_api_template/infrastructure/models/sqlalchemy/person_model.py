# Activate annotations for Python 3.7+ and from __future__ import annotations
from __future__ import annotations

from typing import List

from ksuid import Ksuid
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from web_api_template.core.repository.model.sqlalchemy import Base, BaseModel, Versioned


class PersonModel(BaseModel, Base, Versioned):
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


# Do not import the model here to avoid circular imports
