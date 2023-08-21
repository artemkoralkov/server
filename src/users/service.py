from uuid import uuid4
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from src.users.models import User
from src.users.schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_users(db: Session):
    return db.query(User).all()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def create_user(user: UserCreate, db: Session):
    db.add(
        User(
            id=str(uuid4()),
            username=user.username,
            hashed_password=get_password_hash(user.plain_password),
        )
    )
    db.commit()
    return user


async def login(password: str, db: Session):
    users = db.query(User).all()
    for user in users:
        if verify_password(password, user.hashed_password):
            return user.username


async def delete_user_by_name(username: str, db: Session):
    db.query(User).filter(User.username == username).delete()
    db.commit()
