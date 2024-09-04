
from pydantic import BaseModel, EmailStr
from datetime import datetime


from app.database import Base


"""  POST  """

class PostBase(BaseModel):
    
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


"""  USER  """

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