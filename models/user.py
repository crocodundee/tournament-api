from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, String

from models.base import TimestampedModel


class UserModel(TimestampedModel):
    __tablename__ = "users"

    email = Column(String, nullable=False)
    password_hash = Column(String(length=1024), nullable=True)
    is_active = Column(Boolean, default=True)
