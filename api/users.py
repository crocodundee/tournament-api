from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_session
from models.user import UserModel
from schemas.user import (
    PasswordResetRequestSchema,
    PasswordResetSchema,
    TokenSchema,
    UserCreateSchema,
    UserSchema,
    UserSignInSchema,
)
from services.token_manager import TokenManager
from utils.auth import get_active_user
from utils.email import render_template, send_email

router = APIRouter()


@router.post("/sign-up", response_model=UserSchema, status_code=201)
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
                access_token=TokenManager.generate_access_token(user.id),
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


@router.post("/password-reset", status_code=200)
def password_reset(
    data: PasswordResetRequestSchema,
    background_tasks: BackgroundTasks,
):
    body = render_template(
        "password_reset_email.html",
        {"reset_url": data.build_reset_url()},
    )

    send_email(
        subject="Tournament App - Password Reset",
        recipients=[data.email],
        background_tasks=background_tasks,
        body=body,
        message_type="html",
    )
    return {"message": "If the email exists, a reset link will be sent."}


@router.post("/password-reset-complete", status_code=200)
def password_reset_complete(
    data: PasswordResetSchema,
    session: Session = Depends(get_session),
):
    try:
        payload = TokenManager.parse_token(data.token)
        user_id = payload.get("id")
        user = UserModel.get(session, UserModel.id == user_id)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid token.")
        user.password_hash = UserModel.hash_password(data.new_password1)
        session.commit()
        return {"message": "Password has been reset successfully."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
