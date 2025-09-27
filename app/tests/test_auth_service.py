from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate

def test_register_user_success(db_session):
    repo = UserRepository()
    service = UserService(repo)

    user_data = UserCreate(user_name="Alice", user_email="alice@test.com", password="secret123")
    user = service.register_user(db_session, user_data)

    assert user.user_id is not None
    assert user.user_email == "alice@test.com"

def test_authenticate_user_success(db_session):
    repo = UserRepository()
    service = UserService(repo)

    user_data = UserCreate(user_name="Bob", user_email="bob@test.com", password="secret123")
    service.register_user(db_session, user_data)

    user = service.authenticate_user(db_session, "bob@test.com", "secret123")
    assert user is not None

def test_authenticate_user_failure(db_session):
    repo = UserRepository()
    service = UserService(repo)

    user = service.authenticate_user(db_session, "notfound@test.com", "wrongpass")
    assert user is None
