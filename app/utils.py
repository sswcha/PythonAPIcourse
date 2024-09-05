from passlib.context import CryptContext

# Password encryption
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pw(password: str):
    return pwd_context.hash(password)


def verify_pw(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
