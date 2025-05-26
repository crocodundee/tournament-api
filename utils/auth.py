from typing import Annotated, Optional

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_session
from models.user import UserModel
from services.token_manager import TokenManager


def get_active_user(
    authorization: Annotated[Optional[str], Header()],
    session: Session = Depends(get_session),
) -> UserModel:
    token = authorization.split("Bearer ")[-1]
    if token:
        try:
            payload = TokenManager.parse_token(token)
            user_id = payload.get("id")
            user = UserModel.get(session, UserModel.id == user_id)
            if user and user.is_active:
                return user
        except ValueError as e:
            raise HTTPException(
                detail=str(e),
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
    raise HTTPException(
        detail="You are not authenticated.",
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
