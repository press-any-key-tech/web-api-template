from ksuid import Ksuid
from sqlalchemy import Column, Enum, String

from web_api_template.core.repository.model.sqlalchemy import Base, BaseModel


class PersonModel(Base, BaseModel):
    """Repository persons model

    Args:
        Base (_type_): SQLAlchemy base model
        BaseModel (_type_): base entity model
    """

    __tablename__ = "persons"

    id: str = Column(
        String(27),
        primary_key=True,
        default=lambda: str(Ksuid()),
        index=True,
    )

    name: str = Column(String(500), nullable=False)
    surname: str = Column(String(500), nullable=False)
    email: str = Column(String(500), nullable=False)
