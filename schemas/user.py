from pydantic import BaseModel, EmailStr, model_validator
from typing_extensions import Self

from config.base import FRONTEND_URL
from services.token_manager import TokenManager


class UserCreateSchema(BaseModel):
    email: EmailStr
    password1: str
    password2: str

    @model_validator(mode="after")
    def validate_passwords_match(self) -> Self:
        if self.password1 == self.password2:
            return self
        raise ValueError("Passwords do not match")


class UserSchema(BaseModel):
    email: EmailStr
    is_active: bool


class UserSignInSchema(BaseModel):
    email: EmailStr
    password: str


class TokenSchema(BaseModel):
    access_token: str
    user: UserSchema


class PasswordResetRequestSchema(BaseModel):
    email: EmailStr

    def build_reset_url(self) -> str:
        token = TokenManager.generate_reset_token(self.email.lower())
        return f"{FRONTEND_URL}/reset-password?token={token}"


class PasswordResetSchema(BaseModel):
    token: str
    new_password1: str
    new_password2: str

    @model_validator(mode="after")
    def validate_passwords_match(self) -> Self:
        if self.new_password1 == self.new_password2:
            return self
        raise ValueError("Passwords do not match")
