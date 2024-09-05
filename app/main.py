# Set-ExecutionPolicy Unrestricted -Scope Process
# video link: https://www.youtube.com/watch?v=0sOvCWFmrtA
# timestamp: 7:25:00

import logging
import asyncio
import uvicorn
import os
from time import sleep
from typing import Optional, List

import psycopg2
from psycopg2.extras import RealDictCursor

from fastapi import (
    FastAPI,
    WebSocket,
    Response,
    status,
    WebSocketDisconnect,
    Request,
    HTTPException,
    Depends,
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

import models.logging_config
from models import db_models
from models import db_schemas
from .database import db_engine, get_db
from .utils import *
from routers import post, user, auth

# from modules.ConnectionManager import ConnectionManager


###############################  SETUP  #################################

# fastAPI app
app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
# SQLalchemy
db_models.Base.metadata.create_all(bind=db_engine)
# Logging
logger = logging.getLogger(__name__)


###############################  CONNECT TO DATABASE  #################################
"""
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
"""
##########################################  ROOT  ##########################################


@app.get("/")
def root():
    return {"message": "H rld"}
