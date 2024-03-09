from datetime import datetime
from typing import Optional, cast

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BaseModel:
    """Common model"""

    __tablename__ = "common_base"
    # change your schema here
    # __table_args__ = ({'schema': 'core_schema'})

    created_by = cast(Optional[str], Column(String))
    created_at = cast(
        datetime, Column(DateTime(timezone=False), default=datetime.utcnow())
    )
    updated_by = cast(Optional[str], Column(String))
    updated_at = cast(
        datetime,
        Column(
            DateTime(timezone=False),
            default=datetime.utcnow(),
            onupdate=datetime.utcnow(),
        ),
    )
