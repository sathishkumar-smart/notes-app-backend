# app/routers/notes.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.core.dependencies import get_current_user,get_db
from app.schemas import NoteCreate, NoteUpdate, NoteOut
from app.repositories.note_repository import NoteRepository
from sqlalchemy.orm import Session
from app.models import User 

router = APIRouter()

# Dependency: repository instance (could later be injected with DB session)
def get_note_repository(db: Session = Depends(get_db)) -> NoteRepository:
    return NoteRepository(db)


@router.post("/", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(
    note: NoteCreate,
    repo: NoteRepository = Depends(get_note_repository),
    current_user: User = Depends(get_current_user),  # injected current user
):
    created_note = repo.create(note_create=note, user_id=current_user.user_id)
    return created_note

@router.get("/", response_model=List[NoteOut])
def list_notes(
    repo: NoteRepository = Depends(get_note_repository),
):
    """
    Retrieve all notes.
    """
    return repo.get_all()


@router.get("/{note_id}", response_model=NoteOut)
async def get_note(
    note_id: int,
    repo: NoteRepository = Depends(get_note_repository),
):
    """
    Retrieve a single note by ID.
    """
    note = await repo.get_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=NoteOut)
def update_note(
    note_id: int,
    note_update: NoteUpdate,
    repo: NoteRepository = Depends(get_note_repository),
):
    """
    Update a note by ID.
    """
    updated_note = repo.update( note_id, note_update)
    return updated_note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, repo: NoteRepository = Depends(get_note_repository)):
    deleted = repo.delete(note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"detail": "Note deleted successfully"}