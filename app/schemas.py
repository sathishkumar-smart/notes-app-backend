"""
Pydantic Schemas for request and response validation.

These schemas define the data structures used for API input (requests) and 
output (responses). They enforce strict type validation, ensuring data integrity 
between the client and the server.

Best practices followed:
- Clear separation between input (Create, Update, Login) and output (Out)
- Use of `EmailStr` for stricter email validation
- Optional fields for partial updates
- `orm_mode` enabled for smooth conversion from SQLAlchemy models
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime


# -------------------------
# User Schemas
# -------------------------

class UserBase(BaseModel):
    """
    Base schema for users (shared fields).
    """
    user_name: str
    user_email: EmailStr


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    
    Extends `UserBase` and includes a password field.
    """
    password: str


class UserUpdate(BaseModel):
    """
    Schema for updating an existing user.
    
    - All fields are optional (to allow partial updates).
    """
    user_name: str | None = None
    user_email: EmailStr | None = None


class UserOut(UserBase):
    """
    Schema for returning user data in responses.
    
    Includes metadata such as IDs and timestamps.
    """
    user_id: int
    created_on: datetime
    last_update: datetime | None

    class Config:
        orm_mode = True  # Required for SQLAlchemy model -> Pydantic conversion


class UserLogin(BaseModel):
    """
    Schema for user login requests.
    """
    user_email: EmailStr
    password: str


# -------------------------
# Token Schema
# -------------------------

class Token(BaseModel):
    """
    Schema for JWT authentication token response.
    """
    access_token: str
    token_type: str


# -------------------------
# Note Schemas
# -------------------------

class NoteBase(BaseModel):
    """
    Base schema for notes (shared fields).
    """
    title: str
    body: str | None = None


class NoteCreate(NoteBase):
    """
    Schema for creating a new note.
    """
    pass


class NoteUpdate(NoteBase):
    """
    Schema for updating an existing note.
    
    For now, same fields as base but could be extended later.
    """
    pass


class NoteOut(NoteBase):
    """
    Schema for returning note data in responses.
    
    Includes metadata such as IDs, timestamps, and user reference.
    """
    note_id: int
    user_id: int
    created_on: datetime
    last_update: datetime | None

    class Config:
        orm_mode = True