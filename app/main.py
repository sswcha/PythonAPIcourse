# Set-ExecutionPolicy Unrestricted -Scope Process
# video link: https://www.youtube.com/watch?v=0sOvCWFmrtA
# timestamp: 11:40:00

import logging
import os
from dotenv import load_dotenv

load_dotenv()

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
from fastapi.middleware.cors import CORSMiddleware

import models.logging_config
from models import db_models
from .database import db_engine
from .utils.utils import *
from routers import post, user, auth, root, vote

# from modules.ConnectionManager import ConnectionManager

###############################  SETUP  #################################

# fastAPI app
app = FastAPI()

origins = ["https://www.google.com",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*" ]
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(root.router)
app.include_router(vote.router)

# SQLalchemy, no longer needed bc we use alembic
#db_models.Base.metadata.create_all(bind=db_engine)

# Logging
logger = logging.getLogger(__name__)



uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`