from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'movies.db'}"

engine = create_engine(DATABASE_URL, echo=False) # DATABASE_URL = 'sqlite:///movies.db'

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(bind=engine)
