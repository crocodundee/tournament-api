from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, String

from config.base import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_SECRET
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

    def generate_token(self) -> str:
        """
        Returns access token.
        """
        exp = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload = {"id": self.id, "sub": self.email, "exp": exp}
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
