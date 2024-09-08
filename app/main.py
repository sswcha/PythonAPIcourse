# Set-ExecutionPolicy Unrestricted -Scope Process
# video link: https://www.youtube.com/watch?v=0sOvCWFmrtA
# timestamp: 10:15:00

import logging

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

import models.logging_config
from models import db_models
from .database import db_engine
from .utils.utils import *
from routers import post, user, auth, root, vote

# from modules.ConnectionManager import ConnectionManager

###############################  SETUP  #################################

# fastAPI app
app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(root.router)
app.include_router(vote.router)
# SQLalchemy
db_models.Base.metadata.create_all(bind=db_engine)
# Logging
logger = logging.getLogger(__name__)
