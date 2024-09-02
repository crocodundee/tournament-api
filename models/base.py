from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime, Integer

Base = declarative_base()
metadata = Base.metadata


class BaseModel(Base):
    """Base model for all models."""

    __abstract__ = True

    id = Column(Integer, primary_key=True)


class TimestampedModel(BaseModel):
    """Base model with timestamps."""

    __abstract__ = True

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
