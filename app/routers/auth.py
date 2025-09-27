from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserLogin, Token, UserOut
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.core.dependencies import get_db,get_current_user
from app.core.security import create_access_token

router = APIRouter()

# Initialize repositories and services
user_repo = UserRepository()
user_service = UserService(user_repo)

@router.post("/signup", response_model=UserOut)
def signup(user_create: UserCreate, db: Session = Depends(get_db)):
    """
    User Registration API
    - Creates a new user account if email not already taken.
    - Hashes password before storing.
    """
    existing_user = user_repo.get_by_email(db, user_create.user_email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return user_service.register_user(db, user_create)


@router.post("/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """
    User Login API
    - Validates credentials.
    - Returns JWT access token on success.
    """
    user = user_service.authenticate_user(
        db, user_login.user_email, user_login.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    access_token = create_access_token({"user_id": user.user_id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def get_current_user_profile(current_user=Depends(get_current_user)):
    """
    Get the currently authenticated user's profile.

    - **current_user**: Injected by `get_current_user` dependency
    """
    return current_user