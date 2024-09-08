from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal
from pydantic.types import conint

from app.database import Base


"""  USER  """  # ------------------------------------------


class UserBase(BaseModel):

    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserReturn(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


"""  POST  """  # ------------------------------------------


class PostBase(BaseModel):

    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserReturn

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: Post
    votes_count: int

    class Config:
        from_attributes = True


"""  AUTH  """  # ------------------------------------------


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


"""  VOTES  """  # ------------------------------------------


class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]
