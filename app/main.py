# Set-ExecutionPolicy Unrestricted -Scope Process
# video link: https://www.youtube.com/watch?v=0sOvCWFmrtA
# timestamp: 5:51:20

import logging
import asyncio
import uvicorn
import os
from time import sleep
from typing import Optional, List

import psycopg2
from psycopg2.extras import RealDictCursor

from fastapi import (
    FastAPI, WebSocket, Response, 
    status, WebSocketDisconnect, Request,
    HTTPException, Depends
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

import models.logging_config
from models import db_models
from models import db_schemas
from .database import db_engine, get_db


#from modules.ConnectionManager import ConnectionManager


###############################  SETUP  #################################

# fastAPI app
app = FastAPI()
# SQLalchemy
db_models.Base.metadata.create_all(bind=db_engine)
# Logging
logger = logging.getLogger(__name__)


###############################  CONNECT TO DATABASE  #################################
while True:
    try:
        db_conn = psycopg2.connect(
            host="localhost", 
            database="fastapi", 
            user="postgres",
            password=os.getenv("POSTGRES_PW"),
            cursor_factory=RealDictCursor
            )
        cursor = db_conn.cursor()
        logger.info("Database connection was successful")
        break
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        sleep(2)

##########################################  ROOT  ##########################################

@app.get("/") 
def root():
    return {"message": "H rld"}

##########################################  POSTS  ##########################################

# GET ALL POSTS
@app.get("/posts", status_code=status.HTTP_200_OK, response_model=List[db_schemas.Post])
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(db_models.Post).all()
    return posts


# GET ONE POST
@app.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=db_schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(db_models.Post).filter(db_models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return post


# CREATE ONE POST
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=db_schemas.Post)
def create_post(post: db_schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = db_models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# DELETE ONE POST
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post_query = db.query(db_models.Post).filter(db_models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE ONE POST
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=db_schemas.Post)
def update_post(id: int, post: db_schemas.PostCreate, db: Session = Depends(get_db)):
    
    post_query = db.query(db_models.Post).filter(db_models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()

    