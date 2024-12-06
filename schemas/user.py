from pydantic import BaseModel, EmailStr, model_validator
from typing_extensions import Self


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
