import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv("POSTGRES_CONNECTION")

db_engine = create_engine(SQLALCHEMY_DATABASE_URL)
db_session_local = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

Base = declarative_base()