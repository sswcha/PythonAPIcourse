import logging
from time import sleep
from typing import Optional, List

from fastapi import Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session

import models.logging_config
from models import db_models
from models import db_schemas
from app.database import get_db
from app.utils import *


###############################  SETUP  #################################
# Logging
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/posts", tags=["Posts"])

##########################################  POSTS  ##########################################


# GET ALL POSTS
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[db_schemas.Post])
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(db_models.Post).all()
    return posts


# GET ONE POST
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=db_schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(db_models.Post).filter(db_models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return post


# CREATE ONE POST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=db_schemas.Post)
def create_post(post: db_schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = db_models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# DELETE ONE POST
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post_query = db.query(db_models.Post).filter(db_models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE ONE POST
@router.put(
    "/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=db_schemas.Post
)
def update_post(id: int, post: db_schemas.PostCreate, db: Session = Depends(get_db)):

    post_query = db.query(db_models.Post).filter(db_models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
