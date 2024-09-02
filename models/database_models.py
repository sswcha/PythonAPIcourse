from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import (
    Column, Integer, String, Boolean
)


from app.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)