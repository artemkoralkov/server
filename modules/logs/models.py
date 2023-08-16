from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base


class Log(Base):
    __tablename__ = "logs"
    id: Column = Column(String, primary_key=True, index=True)
    username: Column = Column(String)
    action: Column = Column(String)
    date: Column = Column(DateTime(timezone=True), server_default=func.now())
    lesson_title: Column = Column(String)
    group_name: Column = Column(String)
    teacher_name: Column = Column(String)
    faculty: Column = Column(String)
    lesson_type: Column = Column(String)
    numerator: Column = Column(Boolean)
    denominator: Column = Column(Boolean)
    first_group: Column = Column(Boolean)
    second_group: Column = Column(Boolean)
    day: Column = Column(Integer)
    lesson_number: Column = Column(Integer)
