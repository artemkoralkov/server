from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.database import Base


class Log(Base):
    __tablename__ = "logs"
    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str]
    action: Mapped[str]
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    lesson_title: Mapped[str]
    group_name: Mapped[str]
    teacher_name: Mapped[str]
    faculty: Mapped[str]
    lesson_type: Mapped[str]
    numerator: Mapped[bool]
    denominator: Mapped[bool]
    first_group: Mapped[bool]
    second_group: Mapped[bool]
    day: Mapped[int]
    lesson_number: Mapped[int]
