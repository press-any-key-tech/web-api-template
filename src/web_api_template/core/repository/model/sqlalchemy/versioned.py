from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column, relationship
from sqlalchemy.orm.exc import StaleDataError


@declarative_mixin
class Versioned:
    """Mixin for versioned entities

    Returns:
        _type_: _description_
    """

    version: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
