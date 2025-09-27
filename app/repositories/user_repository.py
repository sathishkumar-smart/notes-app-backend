from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserUpdate
from app.core.security import get_password_hash as hash_password
from typing import Optional, List
from app.db import SessionLocal


class UserRepository:
    """
    Repository layer for User model.
    Encapsulates all DB operations for users.
    """

    # ---------------------------
    # CREATE
    # ---------------------------
    def create(self, db: Session, user_create: UserCreate) -> User:
        """
        Create a new user with hashed password.
        """
        user = User(
            user_name=user_create.user_name,
            user_email=user_create.user_email,
            password=hash_password(user_create.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    # ---------------------------
    # READ
    # ---------------------------
    def get_by_id(self, user_id: int) -> Optional[User]:
         with SessionLocal() as session:
            return session.query(User).filter(User.user_id == user_id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.user_email == email).first()

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    # ---------------------------
    # UPDATE
    # ---------------------------
    def update(self, db: Session, user: User, user_update: UserUpdate) -> User:
        """
        Update existing user fields. Password hashing is handled automatically.
        """
        if user_update.user_name:
            user.user_name = user_update.user_name
        if user_update.user_email:
            user.user_email = user_update.user_email
        if user_update.password:
            user.password_hash = hash_password(user_update.password)

        db.commit()
        db.refresh(user)
        return user

    # ---------------------------
    # DELETE
    # ---------------------------
    def delete(self, db: Session, user: User) -> None:
        db.delete(user)
        db.commit()
