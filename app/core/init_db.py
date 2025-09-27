# app/core/init_db.py
from app.db import Base, engine
from app.models import User
from app.models import Note

Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
