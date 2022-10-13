"""sumary_line

Keyword arguments:
argument -- description
Return: return_description
"""

from itertools import groupby
from pyexpat import model
from uuid import uuid4
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, alias

import models
import schemas


def upload_excel_schedule(db: Session, lessons, faculty):
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    db.query(models.Lesson).filter(models.Lesson.faculty == faculty).delete()
    db.commit()
    for group in lessons:
        i = 1
        j = 0
        if j > 3:
            j = 0
        for days in lessons[group]:
            for lessons_indx in range(len(days)):
                if type(days[lessons_indx]) is list:
                    for lesson in days[lessons_indx]:
                        numerator = 'numerator' in lesson
                        denominator = 'denominator' in lesson
                        first_group = 'first_group' in lesson
                        second_group = 'second_group' in lesson
                        if 'lesson' in lesson:
                            continue
                        teacher_name = lesson['lesson_teacher']
                        if isinstance(teacher_name, list):
                            teacher_name = teacher_name[0]
                        if 'lesson_type' in lesson:
                            lesson_type = lesson['lesson_type']
                        else:
                            lesson_type = ''
                        tmp_lesson = models.Lesson(
                            id=str(uuid4()),
                            lesson_title=lesson['lesson_name'],
                            group_name=group,
                            teacher_name=lesson['lesson_teacher'],
                            lesson_type=lesson_type,
                            faculty=faculty,
                            lesson_number=lessons_indx,
                            day=i,
                            numerator=numerator,
                            denominator=denominator,
                            first_group=first_group,
                            second_group=second_group
                        )
                        db.add(tmp_lesson)
                        db.commit()
                        db.refresh(tmp_lesson)
                else:
                    if 'lesson' in days[lessons_indx]:
                        continue
                    if 'lesson_type' in days[lessons_indx]:
                        lesson_type = days[lessons_indx]['lesson_type']
                    else:
                        lesson_type = ''
                    teacher_name = days[lessons_indx]['lesson_teacher']
                    if isinstance(teacher_name, list):
                        if len(teacher_name) > 2:
                            teacher_name = f'{teacher_name[j]}, {teacher_name[3]}'
                            j += 1
                        else:
                            teacher_name = f'{teacher_name[0]}, {teacher_name[1]}'
                    tmp_lesson = models.Lesson(
                        id=str(uuid4()),
                        lesson_title=days[lessons_indx]['lesson_name'],
                        group_name=group,
                        teacher_name=teacher_name,
                        lesson_type=lesson_type,
                        faculty=faculty,
                        lesson_number=lessons_indx,
                        day=i
                    )
                db.add(tmp_lesson)
                db.commit()
                db.refresh(tmp_lesson)
            i += 1
    return 1


# def get_lessons_by_group(group_name, db: Session):
#     return db.query(models.Lesson).filter(models.Lesson.group_name == group_name).all()


def get_groups_by_faculty(faculty, db: Session):
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    faculty_lessons = db.query(models.Lesson)\
        .filter(models.Lesson.faculty == faculty)\
        .order_by(models.Lesson.group_name).all()
    groups = list({*[i.group_name for i in faculty_lessons]})
    groups.sort()
    return groups


def get_lessons_by_teacher(teacher_name, db: Session):
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """
    teachers_lessons = db.query(models.Lesson)\
        .filter(models.Lesson.teacher_name == teacher_name)\
        .order_by(models.Lesson.day, models.Lesson.lesson_number).all()
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


def get_teachers(db: Session):
    teachers = db.query(models.Teacher).all()
    return teachers


def add_teachers(db: Session, teachers: List[schemas.TeacherCreate]):
    new_teachers = []
    for teacher in teachers:
        tmp_teacher = models.Teacher(**{'id': str(uuid4()), **teacher.dict()})
        new_teachers.append(tmp_teacher)
        db.add(tmp_teacher)
        db.commit()
        db.refresh(tmp_teacher)
    return new_teachers
    
    


def add_teacher(db: Session, teacher: schemas.TeacherCreate):
    tmp_teacher = models.Teacher(**{'id': str(uuid4()), **teacher.dict()})
    db.add(tmp_teacher)
    db.commit()
    db.refresh(tmp_teacher)
    return tmp_teacher


def get_groups(db: Session):
    lessons = db.query(models.Lesson)\
        .order_by(models.Lesson.group_name).all()
    groups = list({*[i.group_name for i in lessons]})
    groups.sort()
    groups = list(map(lambda g: ' '.join([i for i in g.split(' ') if i != '']), groups))
    return groups


def add_lesson(db: Session, lesson: schemas.LessonCreate):
    tmp_lesson = models.Lesson(**{'id':str(uuid4()), **lesson})
    db.add(tmp_lesson)
    db.commit()
    db.refresh(tmp_lesson)
    return tmp_lesson


def get_lessons(db: Session):
    return db.query(models.Lesson).all()


def get_teachers_by_faculty(db: Session, faculty: str):
    teachers_by_faculty = db.query(models.Teacher).filter(
        models.Teacher.faculty == faculty).all()
    # teachers_by_faculty = db.query(models.Lesson).filter(models.Lesson.faculty == faculty).all()
    # teachers_by_faculty = set([i.teacher_name for i in teachers_by_faculty])
    return teachers_by_faculty


def get_lessons_by_group(db: Session, group_name: str):
    group_lessons = db.query(models.Lesson).filter(
        models.Lesson.group_name == group_name).all()
    group_lessons = {
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
    for i in group_lessons:
        for key, group in groupby(group_lessons[i], key=lambda item: vars(item)['lesson_number']):
           
            tmp_group_lessons[i][int(key)].extend(list(group))
    return tmp_group_lessons


def delete_teacher(db: Session, teacher_id):
    db.query(models.Teacher).filter(models.Teacher.id == teacher_id).delete()
    db.commit()


def delete_duplicate_teachers(db: Session):
    inner_q = db.query(func.min(models.Teacher.id)).group_by(models.Teacher.teacher_name)
    aliased = alias(inner_q)
    q = db.query(models.Teacher).filter(~models.Teacher.id.in_(aliased))
    for t in q:
        db.delete(t)
    db.commit()


def delete_lesson(db: Session, lesson_id):
    db.query(models.Lesson).filter(models.Lesson.id == lesson_id).delete()
    db.commit()

def edit_lesson(db: Session, lesson_id, lesson: schemas.Lesson):
    db.query(models.Lesson).filter(models.Lesson.id == lesson_id).update({
        models.Lesson.lesson_title: lesson['lesson_title'],
        models.Lesson.group_name: lesson['group_name'],
        models.Lesson.teacher_name: lesson['teacher_name'],
        models.Lesson.faculty: lesson['faculty'],
        models.Lesson.lesson_type: lesson['lesson_type'],
        models.Lesson.day: int(lesson['day']),
        models.Lesson.lesson_number: lesson['lesson_number'],
        models.Lesson.numerator: lesson['numerator'],
        models.Lesson.denominator: lesson['denominator'],
        models.Lesson.first_group: lesson['first_group'],
        models.Lesson.second_group: lesson['second_group']
        })
    db.commit()
    return {'id': lesson_id, **lesson}
