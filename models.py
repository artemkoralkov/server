
from sqlalchemy import Boolean, Column, Integer, String

from database import Base

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(String, primary_key=True, index=True)
    lesson_title = Column(String, index=True)
    group_name = Column(String, index=True)
    teacher_name = Column(String, index=True)
    faculty = Column(String, index=True)
    lesson_type = Column(String, default='')
    numerator = Column(Boolean, default=False)
    denominator = Column(Boolean, default=False)
    first_group = Column(Boolean, default=False)
    second_group = Column(Boolean, default=False)
    day = Column(Integer, index=True)
    lesson_number = Column(Integer, index=True)



class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(String, primary_key=True, index=True)
    teacher_name = Column(String, index=True, unique=True) 
    faculty = Column(String, index=True)
