import logging
from time import sleep
from typing import Optional, List

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

import models.logging_config
from models import db_models
from models import db_schemas
from app import oauth2
from app.database import get_db
from app.utils.utils import *


###############################  SETUP  #################################
# Logging
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/posts", tags=["Posts"])

##########################################  POSTS  ##########################################


# GET ALL POSTS
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[db_schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):

    # posts = db.query(db_models.Post).filter(db_models.Post.owner_id == current_user.id).all()

    results = (
        db.query(
            db_models.Post, func.count(db_models.Vote.post_id).label("votes_count")
        )
        .join(db_models.Vote, db_models.Vote.post_id == db_models.Post.id, isouter=True)
        .group_by(db_models.Post.id)
        .filter(db_models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return results


# GET ONE POST
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=db_schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(oauth2.get_current_user),
):

    post = (
        db.query(
            db_models.Post, func.count(db_models.Vote.post_id).label("votes_count")
        )
        .join(db_models.Vote, db_models.Vote.post_id == db_models.Post.id, isouter=True)
        .group_by(db_models.Post.id)
        .filter(db_models.Post.id == id)
        .first()
    )
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return post


# CREATE ONE POST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=db_schemas.Post)
def create_post(
    post: db_schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(oauth2.get_current_user),
):
    print(f"printing current_user: {current_user.email}")
    new_post = db_models.Post(**post.model_dump(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# DELETE ONE POST
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(oauth2.get_current_user),
):

    post_query = db.query(db_models.Post).filter(db_models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized to delete a post",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE ONE POST
@router.put(
    "/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=db_schemas.Post
)
def update_post(
    id: int,
    updated_post: db_schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(oauth2.get_current_user),
):

    post_query = db.query(db_models.Post).filter(db_models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized to make changes to a post",
        )

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
