# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load .env file (works locally)
load_dotenv()

DB_USER = os.getenv("DB_USER", "notesuser")
DB_PASS = os.getenv("DB_PASS", "notespass")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")  # local first, later use "db" in docker
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "notesdb")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # auto test connections
    echo=False           # set True for debugging queries
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
