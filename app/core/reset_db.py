from app.db import Base, engine

def reset_database():
    # WARNING: This will drop ALL tables!
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database has been reset!")
