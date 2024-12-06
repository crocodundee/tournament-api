import bcrypt
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, String

from models.base import TimestampedModel


class UserModel(TimestampedModel):
    __tablename__ = "users"

    email = Column(String, nullable=False)
    password_hash = Column(String(length=1024), nullable=True)
    is_active = Column(Boolean, default=True)

    @staticmethod
    def hash_password(password: str):
        """
        Returns hashed password string.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password: str) -> bool:
        """
        Returns True if the password was set to UserModel instance,
        otherwise False.
        """
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
