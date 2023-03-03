"""sumary_line

Keyword arguments:
argument -- description
Return: return_description
"""

from itertools import groupby
from operator import itemgetter
from uuid import uuid4
from sqlalchemy.orm import Session

from .models import Lesson
from .schemas import LessonCreate
from .utils.handle_combined_lessons import handle_combined_lessons


async def upload_excel_schedule(db: Session, schedule, faculty):
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


async def get_lessons_by_teacher(teacher_name: str, db: Session):
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """
    last_name = 0
    for c in teacher_name:
        if c.isupper():
            last_name = teacher_name.find(c)
            break
    teachers_lessons = db.query(Lesson) \
        .filter(Lesson.teacher_name.like(f'%{teacher_name[last_name:]}')) \
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

    for days in tmp_teachers_lessons:
        for lessons_index in range(len(tmp_teachers_lessons[days])):
            lessons = tmp_teachers_lessons[days][lessons_index]
            if len(lessons) >= 2:
                tmp_teachers_lessons[days][lessons_index] = handle_combined_lessons(lessons)
    return tmp_teachers_lessons


async def get_groups(db: Session, faculty=None) -> 'list(dict(str, str))':
    if faculty:
        lessons = db.query(Lesson).filter(Lesson.faculty == faculty) \
            .order_by(Lesson.group_name).all()
    else:
        lessons = db.query(Lesson) \
            .order_by(Lesson.group_name).all()
    groups = [{'group': ' '.join(lesson.group_name.split()), 'faculty': lesson.faculty} for lesson in lessons]
    groups = [dict(t) for t in {tuple(d.items()) for d in groups}]
    groups.sort(key=itemgetter('group'))
    # groups: list[str] = list(map(lambda g: ' '.join(
    #     [i for i in g.split(' ') if i != '']), groups))
    return groups


async def add_lesson(db: Session, lesson: LessonCreate) -> Lesson:
    tmp_lesson: Lesson = Lesson(**{'id': str(uuid4()), **lesson.dict()})
    db.add(tmp_lesson)
    db.commit()
    db.refresh(tmp_lesson)
    return tmp_lesson


async def get_lessons(db: Session) -> 'list[Lesson]':
    return db.query(Lesson).all()


async def get_lessons_by_group(group_name: str, db: Session):
    group_lessons: list[Lesson] = db.query(Lesson).filter(
        Lesson.group_name == group_name).order_by(Lesson.first_group.desc()).all()
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


async def delete_lesson(db: Session, lesson_id):
    db.query(Lesson).filter(Lesson.id == lesson_id).delete()
    db.commit()


async def delete_lessons_by_faculty(db: Session, faculty):
    db.query(Lesson).filter(Lesson.faculty == faculty).delete()
    db.commit()


async def edit_lesson(db: Session, lesson_id, lesson: 'dict[str, str]'):
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
