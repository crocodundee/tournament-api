from typing import Annotated, Optional

import jwt
from fastapi import Depends, Header, HTTPException, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from config.base import JWT_SECRET
from db.session import get_session
from models.user import UserModel


def get_active_user(
    authorization: Annotated[Optional[str], Header()],
    session: Session = Depends(get_session),
) -> UserModel:
    token = authorization.split("Bearer ")[-1]
    if token:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            user_id = payload.get("id")
            user = UserModel.get(session, UserModel.id == user_id)
            if user and user.is_active:
                return user
        except InvalidTokenError:
            pass
    raise HTTPException(
        detail="You are not authenticated.",
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
