from pydantic import BaseModel
from typing import List
from modules.lessons.schemas import Lesson


class RoomReservationBase(BaseModel):
    lesson_id: str
    day: int
    lesson_number: int


class RoomReservationCreate(RoomReservationBase):
    pass


class RoomReservation(RoomReservationBase):
    id: str
    room_id: str

    # lessons: 'list[Lesson]' = []
    class Config:
        orm_mode = True


class RoomBase(BaseModel):
    number: int
    building_number: int = 1
    floor: int
    with_computers: bool = False
    with_projector: bool = False
    max_people: int


class RoomCreate(RoomBase):
    pass


class Room(RoomCreate):
    id: str
    rooms_reservations: List[RoomReservation] = []

    class Config:
        orm_mode = True
