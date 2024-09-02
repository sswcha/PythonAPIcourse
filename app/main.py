# Set-ExecutionPolicy Unrestricted -Scope Process

import logging
import asyncio
import uvicorn
import os
from time import sleep

import psycopg2
from psycopg2.extras import RealDictCursor

from fastapi import (
    FastAPI, WebSocket, Response, 
    status, WebSocketDisconnect, Request,
    HTTPException,
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import models.logging_config
from models import database_schemas, database_models
from .database import db_engine, db_session_local


#from modules.ConnectionManager import ConnectionManager

# fastAPI app
app = FastAPI()
# SQLalchemy
database_models.Base.metadata.create_all(bind=db_engine)
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

# get all posts
@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

# get one post
@app.get("/posts/{id}", status_code=status.HTTP_201_CREATED)
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"data": post}

# create one post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    db_conn.commit()
    return {"data":new_post}

# delete one post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db_conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update one post
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s 
        WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    db_conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return {"data": updated_post}

    