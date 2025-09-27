from sqlalchemy.orm import Session
from app.repositories.note_repository import NoteRepository
from app.schemas import NoteCreate, NoteUpdate

class NoteService:
    """Business logic for Notes"""

    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    def create_note(self, db: Session, note_create: NoteCreate, user_id: int):
        return self.note_repository.create(db, note_create, user_id)

    def get_user_notes(self, db: Session, user_id: int):
        return self.note_repository.list_by_user(db, user_id)

    def update_note(self, db: Session, note, note_update: NoteUpdate):
        return self.note_repository.update(db, note, note_update)

    def delete_note(self, db: Session, note):
        return self.note_repository.delete(db, note)
