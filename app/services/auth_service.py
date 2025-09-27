from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models import User

class AuthService:
    """Service layer handling authentication logic."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, db: Session, name: str, email: str, password: str) -> User:
        existing = self.user_repo.get_by_email(db, email)
        if existing:
            raise ValueError("User already exists")
        hashed_pw = get_password_hash(password)
        return self.user_repo.create(db, {"user_name": name, "user_email": email, "password": hashed_pw})

    def authenticate(self, db: Session, email: str, password: str) -> User | None:
        user = self.user_repo.get_by_email(db, email)
        if user and verify_password(password, user.password):
            return user
        return None

    def generate_token(self, user: User) -> str:
        return create_access_token({"sub": str(user.id)})
