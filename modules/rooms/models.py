from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Room(Base):
    __tablename__ = 'rooms'
    id: Column = Column(String, primary_key=True, index=True)
    number: Column = Column(Integer, index=True)
    building_number: Column = Column(Integer, default=1)
    floor = Column(Integer)
    with_computers = Column(Boolean, default=False)
    with_projector = Column(Boolean, default=False)
    max_people = Column(Integer)
    rooms_reservations = relationship('RoomReservation', back_populates='room')


class RoomReservation(Base):
    __tablename__ = 'rooms_reservation'
    id: Column = Column(String, primary_key=True, index=True)
    room_id = Column(String, ForeignKey('rooms.id'))
    lesson_id = Column(String, ForeignKey('lessons.id'))
    day = Column(Integer)
    lesson_number = Column(Integer)
    
    room = relationship('Room', back_populates='rooms_reservations')
    
