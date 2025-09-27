from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate
from app.core.security import verify_password

class UserService:
    """Business logic for Users"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, db: Session, user_create: UserCreate):
        """Register a new user"""
        return self.user_repository.create(db, user_create)

    def authenticate_user(self, db: Session, email: str, password: str):
        """Validate user credentials"""
        user = self.user_repository.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user
