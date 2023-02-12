"""sumary_line

Keyword arguments:
argument -- description
Return: return_description
"""

from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import func, alias

from .models import Teacher


def get_teachers(db: Session):
    teachers: list[Teacher] = db.query(Teacher).all()
    return teachers


def get_teacher_by_name(db: Session, teacher_name: str):
    return db.query(Teacher).filter(Teacher.teacher_name == teacher_name).first()


def get_teachers_by_faculty(db: Session, faculty: str) -> list[Teacher]:
    teachers_by_faculty: list[Teacher] = db.query(Teacher).filter(
        Teacher.faculty == faculty).all()
    return teachers_by_faculty


def add_teachers(db: Session, teachers) -> list[Teacher]:
    new_teachers: list[Teacher] = []
    for teacher in teachers:
        tmp_teacher: Teacher = Teacher(
            id=str(uuid4()),
            **teacher.dict()
        )
        new_teachers.append(tmp_teacher)
        db.add(tmp_teacher)
        db.commit()
        db.refresh(tmp_teacher)
    return new_teachers


def add_teacher(db: Session, teacher) -> Teacher:
    tmp_teacher: Teacher = Teacher(
        id=str(uuid4()),
        **teacher.dict()
    )
    db.add(tmp_teacher)
    db.commit()
    db.refresh(tmp_teacher)
    return tmp_teacher


def delete_teacher(db: Session, teacher_id) -> None:
    db.query(Teacher).filter(Teacher.id == teacher_id).delete()
    db.commit()


def delete_duplicate_teachers(db: Session) -> None:
    inner_q = db.query(func.min(Teacher.id)).group_by(Teacher.teacher_name)
    aliased = alias(inner_q)
    q = db.query(Teacher).filter(~Teacher.id.in_(aliased))
    for t in q:
        db.delete(t)
    db.commit()
