import os
from dotenv import load_dotenv

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
SQLALCHEMY_DATABASE_URL = os.getenv("POSTGRES_CONNECTION")
ACCESS_TOKEN_EXPIRE_MINUTES = 60
