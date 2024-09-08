import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.utils import constants

# import psycopg2
# from psycopg2.extras import RealDictCursor
# from time import sleep


db_engine = create_engine(constants.SQLALCHEMY_DATABASE_URL)
db_session_local = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

Base = declarative_base()


# Dependency
def get_db():
    db = db_session_local()
    try:
        yield db
    finally:
        db.close()


# code for using psycopg2 for connecting to database, instead of sqlalchemy
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
