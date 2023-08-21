from sqlalchemy import Column, String

from src.database import Base


class User(Base):
    __tablename__ = "users"
    id: Column = Column(String, primary_key=True)
    username: Column = Column(String, unique=True, index=True)
    hashed_password: Column = Column(String)
