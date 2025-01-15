import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime, Integer

Base = declarative_base()
metadata = Base.metadata


class BaseModel(Base):
    """Base model for all models."""

    __abstract__ = True

    id = Column(Integer, primary_key=True)

    @classmethod
    def create(cls, session: Session, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
        return obj

    @classmethod
    def get(cls, session: Session, *args):
        query = sa.select(cls).where(*args).limit(1)
        res = session.execute(query)
        return res.scalars().first()

    @classmethod
    def filter(cls, session: Session, *args):
        query = sa.select(cls).where(*args)
        res = session.execute(query)
        return res.unique().scalars().all()

    @classmethod
    def exists(cls, session: Session, *args) -> bool:
        query = sa.select(sa.select(cls.id).where(*args).exists())
        res = session.execute(query)
        exists = res.scalar()
        return bool(exists)


class TimestampedModel(BaseModel):
    """Base model with timestamps."""

    __abstract__ = True

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
