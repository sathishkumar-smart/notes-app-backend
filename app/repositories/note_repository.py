from sqlalchemy.orm import Session
from app.models import Note
from app.schemas import NoteCreate, NoteUpdate
from typing import Optional, List

class NoteRepository:
    def __init__(self, db: Session):
        self.db = db
        
    """
    Repository layer for Note model.
    Encapsulates all DB operations for notes.
    """

    # ---------------------------
    # CREATE
    # ---------------------------
    def create(self, note_create: NoteCreate, user_id: int) -> Note:
        note = Note(
            title=note_create.title,
            body=note_create.body,
            user_id=user_id
        )
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    # ---------------------------
    # READ
    # ---------------------------
    def get_by_id(self, db: Session, note_id: int) -> Optional[Note]:
        return db.query(Note).filter(Note.note_id == note_id).first()

    def list_by_user(self, db: Session, user_id: int) -> List[Note]:
        return db.query(Note).filter(Note.user_id == user_id).order_by(Note.created_on.desc()).all()

    def get_all(self):
        """Fetch all notes"""
        return self.db.query(Note).all()
    # ---------------------------
    # UPDATE
    # ---------------------------
    def update(self, note_id: int, note_update: NoteUpdate) -> Note:
        note = self.db.query(Note).filter(Note.note_id == note_id).first()
        if not note:
            return None
        if note_update.title:
            note.title = note_update.title
        if note_update.body:
            note.body = note_update.body
        self.db.commit()
        self.db.refresh(note)
        return note


    # ---------------------------
    # DELETE
    # ---------------------------
    def delete(self, note_id: int) -> bool:
        # Use the correct primary key column name
        note = self.db.query(Note).filter(Note.note_id == note_id).first()
        if not note:
            return False  # note doesn't exist

        self.db.delete(note)
        self.db.commit()
        return True
