from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from modules.rooms.models import Room

class Lesson(Base):
    __tablename__ = 'lessons'
    id: Column = Column(String, primary_key=True, index=True)
    room_number: Column = Column(Integer, ForeignKey('rooms.number'))
    lesson_title: Column = Column(String, index=True)
    group_name: Column = Column(String, index=True)
    teacher_name: Column = Column(String, index=True)
    faculty: Column = Column(String, index=True)
    lesson_type: Column = Column(String, default='')
    numerator: Column = Column(Boolean, default=False)
    denominator: Column = Column(Boolean, default=False)
    first_group: Column = Column(Boolean, default=False)
    second_group: Column = Column(Boolean, default=False)
    day: Column = Column(Integer, index=True)
    lesson_number: Column = Column(Integer, index=True)
    
    room = relationship('Room', back_populates='lessons')
