from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session

from database import get_db
from modules.logs.models import Log

logs_router = APIRouter(prefix="/logs", tags=["logs"])


@logs_router.get("", status_code=status.HTTP_200_OK)
async def get_logs(db: Session = Depends(get_db)):
    return db.query(Log).all()
