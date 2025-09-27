from sqlalchemy.orm import Session
from typing import Generic, Type, TypeVar

T = TypeVar("T")  # SQLAlchemy model type

class BaseRepository(Generic[T]):
    """Generic repository for basic CRUD operations."""

    def __init__(self, model: Type[T]):
        self.model = model

    def get(self, db: Session, id: int) -> T | None:
        return db.query(self.model).filter(self.model.id == id).first()

    def list(self, db: Session) -> list[T]:
        return db.query(self.model).all()

    def create(self, db: Session, obj_in: dict) -> T:
        obj = self.model(**obj_in)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: T, obj_in: dict) -> T:
        for field, value in obj_in.items():
            setattr(obj, field, value)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: T):
        db.delete(obj)
        db.commit()
