from pydantic import BaseModel


class UserBase(BaseModel):
    user_id: str
    username: str
    age: int
    email: str


class UserCreate(BaseModel):
    username: str
    age: int
    email: str
    password: str


class PasswordCreate(BaseModel):
    user_id: str
    password_hash: str
