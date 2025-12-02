from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from todo_list_app.config import DATABASE_URL  # بعدا config اضافه میشه

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()