from sqlalchemy.orm import Session
from . import models, schemas
from .core.security import get_password_hash, verify_password

# ---------- Users ----------
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.user_email == email).first()

def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def create_user(db: Session, user_in: schemas.UserCreate):
    hashed = get_password_hash(user_in.password)
    db_user = models.User(user_name=user_in.user_name, user_email=user_in.user_email, password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

# ---------- Notes ----------
def create_note(db: Session, user_id: str, note_in: schemas.NoteCreate):
    db_note = models.Note(user_id=user_id, note_title=note_in.note_title, note_content=note_in.note_content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_notes_for_user(db: Session, user_id: str):
    return db.query(models.Note).filter(models.Note.user_id == user_id).order_by(models.Note.last_update.desc()).all()

def get_note(db: Session, note_id: str, user_id: str):
    return db.query(models.Note).filter(models.Note.note_id == note_id, models.Note.user_id == user_id).first()

def update_note(db: Session, note_obj: models.Note, note_in: schemas.NoteUpdate):
    if note_in.note_title is not None:
        note_obj.note_title = note_in.note_title
    if note_in.note_content is not None:
        note_obj.note_content = note_in.note_content
    db.commit()
    db.refresh(note_obj)
    return note_obj

def delete_note(db: Session, note_obj: models.Note):
    db.delete(note_obj)
    db.commit()
    return True
