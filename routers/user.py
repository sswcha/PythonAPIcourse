import logging
from time import sleep
from typing import Optional, List

from fastapi import Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session

import models.logging_config
from models import db_models
from models import db_schemas
from app.database import get_db
from app.utils.utils import *


###############################  SETUP  #################################
# Logging
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users", tags=["Users"])

##########################################  USERS  ##########################################


# GET ALL USERS
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[db_schemas.User])
def get_users(db: Session = Depends(get_db)):

    users = db.query(db_models.User).all()
    return users


# GET ONE USER
@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=db_schemas.UserReturn
)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(db_models.User).filter(db_models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


# CREATE ONE USER
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=db_schemas.UserReturn
)
def create_user(user: db_schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password
    user.password = hash_pw(user.password)

    existing_user = (
        db.query(db_models.User).filter(db_models.User.email == user.email).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already in use"
        )
    new_user = db_models.User(**user.model_dump())
    db.add(new_user)

    db.commit()
    db.refresh(new_user)
    return new_user


# DELETE ONE USER
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):

    user_query = db.query(db_models.User).filter(db_models.User.id == id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE ONE USER
@router.put(
    "/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=db_schemas.User
)
def update_user(id: int, user: db_schemas.UserCreate, db: Session = Depends(get_db)):

    user_query = db.query(db_models.User).filter(db_models.User.id == id)

    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user_query.update(user.model_dump(), synchronize_session=False)
    db.commit()
    return user_query.first()
