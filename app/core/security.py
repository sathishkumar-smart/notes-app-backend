from passlib.context import CryptContext
from jose import jwt, JWTError
import os
from datetime import datetime, timedelta
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

def get_password_hash(password):
    """
    Hash a plain password using bcrypt.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    
def verify_access_token(token: str):
    """
    Verify JWT token and return payload.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")