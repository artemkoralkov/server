from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    plain_password: str


class User(UserBase):
    id: str
    hashed_password: str

    class Config:
        orm_mode = True
