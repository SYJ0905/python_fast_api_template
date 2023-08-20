from pydantic import BaseModel


class UserBase(BaseModel):
    user_id: str
    username: str
    age: int
    email: str

    # class Config:
    #     from_attributes = True
    #     # orm_mode = True


class UserCreate(BaseModel):
    username: str
    age: int
    email: str
    password: str


# class PasswordBase(BaseModel):
#     user_id: str
#     userpassword_hashname: str

#     class Config:
#         from_attributes = True
#         # orm_mode = True
