from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Lesson(Base):
    __tablename__ = "lessons"
    id: Mapped[str] = mapped_column(primary_key=True)
    lesson_title: Mapped[str]
    group_name: Mapped[str]
    teacher_name: Mapped[str]
    faculty: Mapped[str]
    lesson_type: Mapped[str] = mapped_column(default="")
    numerator: Mapped[bool] = mapped_column(default=False)
    denominator: Mapped[bool] = mapped_column(Boolean, default=False)
    first_group: Mapped[bool] = mapped_column(Boolean, default=False)
    second_group: Mapped[bool] = mapped_column(Boolean, default=False)
    day: Mapped[int]
    lesson_number: Mapped[int]
