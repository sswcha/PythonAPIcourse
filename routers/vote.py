import logging
from time import sleep
from typing import Optional, List

from fastapi import Response, status, HTTPException, Depends, APIRouter

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
router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: db_schemas.Vote,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(oauth2.get_current_user),
):
    found_post = (
        db.query(db_models.Post).filter(db_models.Post.id == vote.post_id).first()
    )
    if not found_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {vote.post_id} not found",
        )

    vote_query = db.query(db_models.Vote).filter(
        db_models.Vote.post_id == vote.post_id,
        db_models.Vote.user_id == current_user.id,
    )
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already votes on post {vote.post_id}",
            )
        new_vote = db_models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}
