from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    email: str
    password: str


class UserSchema(BaseModel):
    email: str
    is_active: bool
