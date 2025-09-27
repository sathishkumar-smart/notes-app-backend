"""
SQLAlchemy ORM Models for the Notes App.

This module defines the core database entities (`User` and `Note`) using
SQLAlchemy's declarative ORM approach. Each model is mapped to a database table
with clearly defined fields, constraints, and relationships.

Best practices followed:
- Meaningful table and column names
- Constraints for data integrity (unique, non-nullable)
- Timestamps for auditing (created_on, last_update)
- Clear separation of concerns (models only contain schema definitions)
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from .db import Base


class User(Base):
    """
    User model representing application users.

    Attributes:
        user_id (int): Primary key, unique identifier for the user.
        user_name (str): Full name of the user.
        user_email (str): Unique email used for authentication.
        password_hash (str): Hashed password string (never store plain text!).
        created_on (datetime): Timestamp when the user was created.
        last_update (datetime): Timestamp of the most recent update.
    """

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)
    user_email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    created_on = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_update = Column(
        DateTime(timezone=True), onupdate=func.now()
    )


class Note(Base):
    """
    Note model representing notes created by users.

    Attributes:
        note_id (int): Primary key, unique identifier for the note.
        title (str): Title of the note (required).
        body (str): Content of the note (optional).
        user_id (int): Foreign key reference to the `users` table.
        created_on (datetime): Timestamp when the note was created.
        last_update (datetime): Timestamp of the most recent update.
    """

    __tablename__ = "notes"

    note_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=True)
    user_id = Column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    created_on = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_update = Column(
        DateTime(timezone=True), onupdate=func.now()
    )