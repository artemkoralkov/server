from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Room(Base):
    __tablename__ = 'rooms'
    number: Column = Column(Integer, primary_key=True, index=True)
    building_number: Column = Column(Integer, default=1)
    floor = Column(Integer)
    with_computers = Column(Boolean, default=False)
    with_projector = Column(Boolean, default=False)
    max_people = Column(Integer)
    # rooms_reservations = relationship('RoomReservation', back_populates='room')
    lessons = relationship('Lesson', back_populates='room')

# class RoomReservation(Base):
#     __tablename__ = 'rooms_reservation'
#     id: Column = Column(String, primary_key=True, index=True)
#     day = Column(Integer)
#     lesson_number = Column(Integer)

