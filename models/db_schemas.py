
from pydantic import BaseModel


from app.database import Base

class PostBase(BaseModel):
    
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: str
    class Config:
        from_attributes = True