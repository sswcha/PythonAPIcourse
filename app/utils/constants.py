import os
from dotenv import load_dotenv

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri != None:
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URL = uri
else:
    SQLALCHEMY_DATABASE_URL = os.getenv("POSTGRES_CONNECTION")
#SQLALCHEMY_DATABASE_URL = os.getenv("POSTGRES_CONNECTION")
ACCESS_TOKEN_EXPIRE_MINUTES = 60
