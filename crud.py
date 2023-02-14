"""sumary_line

Keyword arguments:
argument -- description
Return: return_description
"""

from itertools import groupby
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import func, alias

from models import Lesson, Teacher
from is_teahcer_lessons_equal import is_teahcer_lessons_equal
import schemas


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


def get_groups_by_faculty(faculty, db: Session):
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    faculty_lessons = db.query(Lesson) \
        .filter(Lesson.faculty == faculty) \
        .order_by(Lesson.group_name).all()
    groups = list({*[i.group_name for i in faculty_lessons]})
    groups.sort()
    return groups


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
    print(tmp_teachers_lessons['Saturday'])
    for days in tmp_teachers_lessons:
        for lessons_index in range(len(tmp_teachers_lessons[days])):
            lessons = tmp_teachers_lessons[days][lessons_index]
            if len(lessons) == 2:
                first_lesson_dict = lessons[0].__dict__
                second_lesson_dict = lessons[1].__dict__
                if is_teahcer_lessons_equal(first_lesson_dict, second_lesson_dict):
                    group = f'{first_lesson_dict["group_name"]}, {second_lesson_dict["group_name"]}'
                    id = f'{first_lesson_dict["id"]}, {second_lesson_dict["id"]}'
                    del first_lesson_dict["id"]
                    del first_lesson_dict['group_name']
                    del first_lesson_dict['_sa_instance_state']
                    tmp_teachers_lessons[days][lessons_index] = [
                        Lesson(
                            id = id,
                            group_name = group,
                            **first_lesson_dict,
                            
                        )
                    ] 
    print(tmp_teachers_lessons['Saturday'])
    return tmp_teachers_lessons


def get_teachers(db: Session) -> 'list[Teacher]':
    teachers: list[Teacher] = db.query(Teacher).all()
    return teachers


def get_teacher_by_name(db: Session, teacher_name: str):
    return db.query(Teacher).filter(Teacher.teacher_name == teacher_name).first()


def get_teachers_by_faculty(db: Session, faculty: str) -> 'list[Teacher]':
    teachers_by_faculty: list[Teacher] = db.query(Teacher).filter(
        Teacher.faculty == faculty).all()
    return teachers_by_faculty


def add_teachers(db: Session, teachers: 'list[schemas.TeacherCreate]') -> 'list[Teacher]':
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


def add_teacher(db: Session, teacher: schemas.TeacherCreate) -> Teacher:
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


def get_groups(db: Session) -> 'list[str]':
    lessons = db.query(Lesson) \
        .order_by(Lesson.group_name).all()
    groups = list({*[lesson.group_name for lesson in lessons]})
    groups.sort()
    groups: list[str] = list(map(lambda g: ' '.join(
        [i for i in g.split(' ') if i != '']), groups))
    return groups


def add_lesson(db: Session, lesson: schemas.LessonCreate) -> Lesson:
    tmp_lesson: Lesson = Lesson(**{'id': str(uuid4()), **lesson.dict()})
    db.add(tmp_lesson)
    db.commit()
    db.refresh(tmp_lesson)
    return tmp_lesson


def get_lessons(db: Session) -> 'list[Lesson]':
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


def edit_lesson(db: Session, lesson_id, lesson: 'dict[str, str]'):
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
