from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,sessionmaker

DATABASE_URL = "postgresql://postgres:secret@localhost:5432/my_db"

engine = create_engine(DATABASE_URL,echo=True)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as session:
        yield session
