# app/core/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_PREFIX = "/api"
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # JWT Config
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # DB Config
    DB_USER = os.getenv("DB_USER", "notesuser")
    DB_PASS = os.getenv("DB_PASS", "notespass")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "notesdb")
    DB_ECHO = os.getenv("DB_ECHO", "false").lower() == "true"

settings = Settings()
