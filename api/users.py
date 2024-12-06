from fastapi import APIRouter, Depends
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session

from db.session import get_session
from models.user import UserModel
from schemas.user import UserCreateSchema, UserSchema

router = APIRouter()


@router.post("/sign-up", response_model=UserSchema)
def sign_up(user: UserCreateSchema, session: Session = Depends(get_session)):
    data = dict(user)
    user = UserModel.filter(session, UserModel.email == data["email"])
    if user:
        raise RequestValidationError(
            errors=[
                {
                    "loc": ["email"],
                    "msg": "User with this email already exists.",
                    "type": "value_error",
                }
            ]
        )
    return UserModel.create(
        session,
        email=data["email"],
        password_hash=UserModel.hash_password(data["password1"]),
    )
