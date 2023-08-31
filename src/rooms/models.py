from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base


class Room(Base):
    __tablename__ = "rooms"
    id: Mapped[str] = mapped_column(primary_key=True)
    number: Mapped[int]
    building_number: Mapped[int] = mapped_column(default=1)
    floor: Mapped[int]
    with_computers: Mapped[bool] = mapped_column(default=False)
    with_projector: Mapped[bool] = mapped_column(default=False)
    max_people: Mapped[int]
    rooms_reservations = relationship("RoomReservation", back_populates="room")


class RoomReservation(Base):
    __tablename__ = "rooms_reservation"
    id: Mapped[str] = mapped_column(primary_key=True)
    room_id: Mapped[str] = mapped_column(ForeignKey("rooms.id"))
    lesson_id: Mapped[str] = mapped_column(ForeignKey("lessons.id"))
    day: Mapped[int]
    lesson_number: Mapped[int]
    room = relationship("Room", back_populates="rooms_reservations")
