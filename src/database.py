import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.config import settings

# SQLALCHEMY_DATABASE_URL = "sqlite:///sql_app.db"
SQLALCHEMY_DATABASE_URL = settings.SQLITE_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# Base = declarative_base()
Base.metadata.create_all(engine, checkfirst=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
