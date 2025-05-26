from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt

from config.base import JWT_ALGORITHM, JWT_SECRET


class TokenManager:

    @staticmethod
    def generate_access_token(user_id: int, expires_in_hours: int = 1) -> str:
        payload = {
            "id": user_id,
            "type": "access_token",
            "exp": datetime.now(timezone.utc) + timedelta(hours=expires_in_hours),
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    @staticmethod
    def generate_reset_token(email: str, expires_in_hours: int = 1) -> str:
        payload = {
            "email": email,
            "type": "password_reset",
            "exp": datetime.now(timezone.utc) + timedelta(hours=expires_in_hours),
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    @staticmethod
    def generate_verification_token(email: str, expires_in_days: int = 7) -> str:
        payload = {
            "email": email,
            "type": "email_verification",
            "exp": datetime.now(timezone.utc) + timedelta(days=expires_in_days),
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    @staticmethod
    def parse_token(token: str) -> Dict[Any, Any]:
        try:
            return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
