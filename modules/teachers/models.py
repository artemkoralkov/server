from sqlalchemy import Column, String

from database import Base


class Teacher(Base):
    __tablename__ = 'teachers'
    __table_args__ = {'extend_existing': True}
    id: Column = Column(String, primary_key=True, index=True)
    teacher_name: Column = Column(String, index=True, unique=True)
    faculty: Column = Column(String, index=True)
