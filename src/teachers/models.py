from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Teacher(Base):
    __tablename__ = "teachers"
    __table_args__ = {"extend_existing": True}
    id: Mapped[str] = mapped_column(primary_key=True)
    teacher_name: Mapped[str] = mapped_column(unique=True)
    faculty: Mapped[str]
