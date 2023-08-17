from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

import modules.rooms.crud as crud
from database import get_db
from modules.rooms.schemas import RoomCreate, Room, RoomReservationCreate

rooms_router = APIRouter(prefix="/rooms", tags=["rooms"])


@rooms_router.get("", response_model=List[Room])
async def get_rooms(db: Session = Depends(get_db)):
    return await crud.get_rooms(db)


@rooms_router.get("/reservations")
async def get_rooms_reservations(db: Session = Depends(get_db)):
    return await crud.get_rooms_reservations(db)


@rooms_router.get("/{room_number}", response_model=Room)
async def get_room_by_number(room_number: int, db: Session = Depends(get_db)):
    return await crud.get_room_by_number(db, room_number)


@rooms_router.post("")
async def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    return await crud.create_room(db, room)


@rooms_router.post("/reservations/{room_id}")
async def create_room_reservation(
    room_id: str, room_reservation: RoomReservationCreate, db: Session = Depends(get_db)
):
    return await crud.create_room_reservation(db, room_reservation, room_id)


@rooms_router.delete("/{room_id}")
async def delete_room(room_id: str, db: Session = Depends(get_db)):
    return await crud.delete_room(db, room_id)


@rooms_router.delete("/reservations/{reservation_id}")
async def delete_room_reservation(reservation_id: str, db: Session = Depends(get_db)):
    return await crud.delete_room_reservation(db, reservation_id)
