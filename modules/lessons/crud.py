"""sumary_line

Keyword arguments:
argument -- description
Return: return_description
"""

from itertools import groupby
from uuid import uuid4
from sqlalchemy.orm import Session

from .models import Lesson
from .schemas import *


def upload_excel_schedule(db: Session, schedule, faculty):
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    db.query(Lesson).filter(Lesson.faculty == faculty).delete()
    db.commit()
    for group, days in schedule.items():
        day = 1
        for lessons in days:
            lesson_number = -1
            for lesson in lessons:
                lesson_number += 1
                if isinstance(lesson, list):
                    for i in lesson:
                        if 'lesson' in i:
                            continue
                        tmp_lesson = Lesson(
                            id=str(uuid4()),
                            day=day,
                            lesson_number=lesson_number,
                            group_name=group,
                            faculty=faculty,
                            **i
                        )
                        db.add(tmp_lesson)
                        db.commit()
                        db.refresh(tmp_lesson)
                else:
                    if 'lesson' in lesson:
                        continue
                    tmp_lesson = Lesson(
                        id=str(uuid4()),
                        day=day,
                        lesson_number=lesson_number,
                        group_name=group,
                        faculty=faculty,
                        **lesson
                    )
                    db.add(tmp_lesson)
                    db.commit()
                    db.refresh(tmp_lesson)
            day += 1
    return 1


def get_lessons_by_teacher(teacher_name: str, db: Session):
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """
    teachers_lessons = db.query(Lesson) \
        .filter(Lesson.teacher_name.like(f'%{teacher_name}')) \
        .order_by(Lesson.day, Lesson.lesson_number).all()
    teachers_lessons = {
        'Monday': [i for i in teachers_lessons if i.day == 1],
        'Tuesday': [i for i in teachers_lessons if i.day == 2],
        'Wednesday': [i for i in teachers_lessons if i.day == 3],
        'Thursday': [i for i in teachers_lessons if i.day == 4],
        'Friday': [i for i in teachers_lessons if i.day == 5],
        'Saturday': [i for i in teachers_lessons if i.day == 6],
    }

    tmp_teachers_lessons = {
        'Monday': [[], [], [], [], [], []],
        'Tuesday': [[], [], [], [], [], []],
        'Wednesday': [[], [], [], [], [], []],
        'Thursday': [[], [], [], [], [], []],
        'Friday': [[], [], [], [], [], []],
        'Saturday': [[], [], [], [], [], []],
    }
    for i in teachers_lessons:
        for key, group in groupby(teachers_lessons[i], key=lambda item: vars(item)['lesson_number']):
            tmp_teachers_lessons[i][int(key)].extend(list(group))

    return tmp_teachers_lessons


def get_groups(db: Session) -> list[str]:
    lessons = db.query(Lesson) \
        .order_by(Lesson.group_name).all()
    groups = list({*[lesson.group_name for lesson in lessons]})
    groups.sort()
    groups: list[str] = list(map(lambda g: ' '.join(
        [i for i in g.split(' ') if i != '']), groups))
    return groups


def add_lesson(db: Session, lesson: LessonCreate) -> Lesson:
    tmp_lesson: Lesson = Lesson(**{'id': str(uuid4()), **lesson.dict()})
    db.add(tmp_lesson)
    db.commit()
    db.refresh(tmp_lesson)
    return tmp_lesson


def get_lessons(db: Session) -> list[Lesson]:
    return db.query(Lesson).all()


def get_lessons_by_group(db: Session, group_name: str):
    group_lessons: list[Lesson] = db.query(Lesson).filter(
        Lesson.group_name == group_name).all()
    group_lessons_by_days: dict[str, list[Lesson]] = {
        'Monday': [i for i in group_lessons if i.day == 1],
        'Tuesday': [i for i in group_lessons if i.day == 2],
        'Wednesday': [i for i in group_lessons if i.day == 3],
        'Thursday': [i for i in group_lessons if i.day == 4],
        'Friday': [i for i in group_lessons if i.day == 5],
        'Saturday': [i for i in group_lessons if i.day == 6],
    }
    tmp_group_lessons = {
        'Monday': [[], [], [], [], [], []],
        'Tuesday': [[], [], [], [], [], []],
        'Wednesday': [[], [], [], [], [], []],
        'Thursday': [[], [], [], [], [], []],
        'Friday': [[], [], [], [], [], []],
        'Saturday': [[], [], [], [], [], []],
    }
    for i in group_lessons_by_days:
        for key, group in groupby(group_lessons_by_days[i], key=lambda item: vars(item)['lesson_number']):
            tmp_group_lessons[i][int(key)].extend(list(group))
    return tmp_group_lessons


def delete_lesson(db: Session, lesson_id):
    db.query(Lesson).filter(Lesson.id == lesson_id).delete()
    db.commit()


def edit_lesson(db: Session, lesson_id, lesson: dict[str, str]):
    db.query(Lesson).filter(Lesson.id == lesson_id).update({
        Lesson.lesson_title: lesson['lesson_title'],
        Lesson.group_name: lesson['group_name'],
        Lesson.teacher_name: lesson['teacher_name'],
        Lesson.faculty: lesson['faculty'],
        Lesson.lesson_type: lesson['lesson_type'],
        Lesson.day: int(lesson['day']),
        Lesson.lesson_number: lesson['lesson_number'],
        Lesson.numerator: lesson['numerator'],
        Lesson.denominator: lesson['denominator'],
        Lesson.first_group: lesson['first_group'],
        Lesson.second_group: lesson['second_group']
    })
    db.commit()
    return {'id': lesson_id, **lesson}
