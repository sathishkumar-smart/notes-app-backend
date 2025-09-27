from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import User
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_access_token
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Extract user from JWT token (synchronous).

    Raises 401 if token is invalid or user not found.
    """
    payload = verify_access_token(token)
    user_id = payload.get("user_id")

    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication token")

    user_repo = UserRepository()
    user = user_repo.get_by_id(user_id)  # sync call

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User not found")

    return user
