from uuid import uuid4
from sqlalchemy.orm import Session
from fastapi import HTTPException

from .models import Room, RoomReservation
from .schemas import RoomCreate, RoomReservationCreate


async def get_rooms(db: Session):
    return db.query(Room).all()


async def get_room_by_number(db: Session, room_number: int):
    r = db.query(Room).first()
    return db.query(Room).filter(Room.number == room_number).first()


async def get_rooms_reservations(db: Session):
    return db.query(RoomReservation).all()


async def create_room(db: Session, room: RoomCreate):
    room_db = Room(**room.dict(), id = str(uuid4()))
    db.add(room_db)
    db.commit()
    db.refresh(room_db)
    return room_db

async def create_room_reservation(db: Session, room_reservation: RoomReservationCreate, room_id: str):
    db_room_reservation = db.query(RoomReservation).filter(
        RoomReservation.room_id == room_id,
        RoomReservation.day == room_reservation.day,
        RoomReservation.lesson_number == room_reservation.lesson_number
        ).first()
    print(db_room_reservation)
    if db_room_reservation is not None:
        raise HTTPException(status_code=403, detail='Room already reserved')
    else:
        db_item = RoomReservation(**room_reservation.dict(), room_id=room_id, id=str(uuid4()))
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item


async def delete_room(db: Session, room_id: str):
    db.query(Room).filter(Room.id == room_id).delete()
    db.commit()

async def delete_room_reservation(db: Session, reservation_id: str):
    db.query(RoomReservation).filter(RoomReservation.id == reservation_id).delete()
    db.commit()

