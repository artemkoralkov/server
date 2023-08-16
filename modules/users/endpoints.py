from fastapi import Depends, APIRouter, status
from fastapi.params import Body
from sqlalchemy.orm import Session

import modules.users.crud as crud
from database import get_db
from modules.users.schemas import UserCreate

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("", status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db)):
    return await crud.get_users(db)


@users_router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return await crud.create_user(user, db)


@users_router.post("/login")
async def login(password: str = Body(..., embed=True), db: Session = Depends(get_db)):
    return await crud.login(password, db)


@users_router.delete("")
async def delete_user(
    username: str = Body(..., embed=True), db: Session = Depends(get_db)
):
    await crud.delete_user_by_name(username, db)
