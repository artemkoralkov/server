from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import func, alias, select

from src.teachers.exceptions import TeacherAlreadyExists, TeacherNotFound
from src.teachers.models import Teacher


async def get_teachers(db: Session):
    return db.query(Teacher).all()


async def get_teacher_by_name(db: Session, teacher_name: str):
    return db.query(Teacher).filter(Teacher.teacher_name == teacher_name).first()


async def get_teachers_by_faculty(db: Session, faculty: str):
    return db.query(Teacher).filter(Teacher.faculty == faculty).all()


async def add_teachers(db: Session, teachers):
    new_teachers = []
    for teacher in teachers:
        tmp_teacher: Teacher = Teacher(id=str(uuid4()), **teacher.dict())
        new_teachers.append(tmp_teacher)
        db.add(tmp_teacher)
        db.commit()
        db.refresh(tmp_teacher)
    return new_teachers


async def add_teacher(db: Session, teacher) -> Teacher:
    db_teacher = await get_teacher_by_name(db, teacher.teacher_name)
    if db_teacher:
        raise TeacherAlreadyExists
    tmp_teacher: Teacher = Teacher(id=str(uuid4()), **teacher.dict())
    db.add(tmp_teacher)
    db.commit()
    db.refresh(tmp_teacher)
    return tmp_teacher


async def delete_teacher(db: Session, teacher_id) -> None:
    teacher = db.scalars(select(Teacher).where(Teacher.id == teacher_id)).one_or_none()
    if not teacher:
        raise TeacherNotFound
    db.delete(teacher)
    # db.query(Teacher).filter(Teacher.id == teacher_id).delete()
    db.commit()


async def delete_duplicate_teachers(db: Session) -> None:
    inner_q = db.query(func.min(Teacher.id)).group_by(Teacher.teacher_name)
    aliased = alias(inner_q)
    q = db.query(Teacher).filter(~Teacher.id.in_(aliased))
    for t in q:
        db.delete(t)
    db.commit()
