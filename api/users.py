from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_session
from models.user import UserModel
from schemas.user import TokenSchema, UserCreateSchema, UserSchema, UserSignInSchema
from utils.auth import get_active_user

router = APIRouter()


@router.post("/sign-up", response_model=UserSchema)
def sign_up(user: UserCreateSchema, session: Session = Depends(get_session)):
    data = dict(user)
    user = UserModel.get(session, UserModel.email == data["email"])
    if user:
        raise HTTPException(
            detail="User with this email already exist.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return UserModel.create(
        session,
        email=data["email"],
        password_hash=UserModel.hash_password(data["password1"]),
    )


@router.post("/sign-in", response_model=TokenSchema)
def sign_in(user: UserSignInSchema, session: Session = Depends(get_session)):
    data = dict(user)
    user = UserModel.get(session, UserModel.email == data["email"])
    if user:
        if user.check_password(data["password"]):
            return TokenSchema(
                access_token=user.generate_token(),
                user=UserSchema(email=user.email, is_active=user.is_active),
            )
        raise HTTPException(
            detail="Invalid password.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    raise HTTPException(
        detail="User does not exist.",
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@router.get("/me", response_model=UserSchema)
def me(user: Optional[UserModel] = Depends(get_active_user)):
    return user
