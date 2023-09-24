import datetime
import os
from operator import itemgetter
from uuid import uuid4

from sqlalchemy.orm import Session

from src.lessons.models import Lesson
from src.lessons.schemas import LessonCreate, Lesson as PydanticLesson
from src.lessons.utils.excel_to_json import excel_to_json
from src.lessons.utils.get_day_display import get_day_display
from src.lessons.utils.handle_combined_lessons import handle_combined_lessons
from src.logs.models import Log


async def upload_excel_schedule(db: Session, file, faculty):
    # Сохраняем содержимое файла в памяти, чтобы избежать записи на диск
    with open(file.filename, "wb+") as file_object:
        file_object.write(file.file.read())

    # Преобразуем содержимое файла в JSON
    schedule = excel_to_json(file.filename, faculty)
    os.remove(file.filename)

    # Очищаем базу данных от старых данных для указанного факультета
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
                        if "lesson" in i:
                            continue
                        if isinstance(i["teacher_name"], list):
                            for teacher in i["teacher_name"]:
                                tmp_lesson = Lesson(
                                    id=str(uuid4()),
                                    day=day,
                                    lesson_number=lesson_number,
                                    group_name=group,
                                    faculty=faculty,
                                    teacher_name=teacher,
                                    lesson_type=i["lesson_type"],
                                    lesson_title=i["lesson_title"],
                                    numerator=i.get("numerator", False),
                                    denominator=i.get("denominator", False),
                                    first_group=i.get("first_group", False),
                                    second_group=i.get("second_group", False),
                                )
                                db.add(tmp_lesson)
                                db.commit()
                                db.refresh(tmp_lesson)
                        else:
                            tmp_lesson = Lesson(
                                id=str(uuid4()),
                                day=day,
                                lesson_number=lesson_number,
                                group_name=group,
                                faculty=faculty,
                                **i,
                            )
                            db.add(tmp_lesson)
                            db.commit()
                            db.refresh(tmp_lesson)
                else:
                    if "lesson" in lesson:
                        continue
                    if isinstance(lesson["teacher_name"], list):
                        for teacher in lesson["teacher_name"]:
                            tmp_lesson = Lesson(
                                id=str(uuid4()),
                                day=day,
                                lesson_number=lesson_number,
                                group_name=group,
                                faculty=faculty,
                                teacher_name=teacher,
                                lesson_type=lesson["lesson_type"],
                                lesson_title=lesson["lesson_title"],
                                numerator=lesson.get("numerator", False),
                                denominator=lesson.get("denominator", False),
                                first_group=lesson.get("first_group", False),
                                second_group=lesson.get("second_group", False),
                            )
                            db.add(tmp_lesson)
                            db.commit()
                            db.refresh(tmp_lesson)
                    else:
                        tmp_lesson = Lesson(
                            id=str(uuid4()),
                            day=day,
                            lesson_number=lesson_number,
                            group_name=group,
                            faculty=faculty,
                            **lesson,
                        )
                        db.add(tmp_lesson)
                        db.commit()
                        db.refresh(tmp_lesson)
            day += 1
    return 1


async def get_lessons_by_teacher(teacher_name: str, db: Session):
    last_name_start_index = next(
        (i for i, c in enumerate(teacher_name) if c.isupper()), 0
    )
    teachers_lessons = (
        db.query(Lesson)
        .filter(Lesson.teacher_name.like(f"%{teacher_name[last_name_start_index:]}%"))
        .order_by(Lesson.day, Lesson.lesson_number)
        .all()
    )

    tmp_teachers_lessons = {
        "Monday": [[] for _ in range(6)],
        "Tuesday": [[] for _ in range(6)],
        "Wednesday": [[] for _ in range(6)],
        "Thursday": [[] for _ in range(6)],
        "Friday": [[] for _ in range(6)],
        "Saturday": [[] for _ in range(6)],
    }

    for lesson in teachers_lessons:
        day = lesson.day
        lesson_number = lesson.lesson_number
        tmp_teachers_lessons[get_day_display(day)][lesson_number].append(lesson)

    for days in tmp_teachers_lessons:
        for lessons_index in range(len(tmp_teachers_lessons[days])):
            lessons = tmp_teachers_lessons[days][lessons_index]
            if len(lessons) >= 2:
                tmp_teachers_lessons[days][lessons_index] = handle_combined_lessons(
                    lessons, "teacher"
                )

    return tmp_teachers_lessons


async def get_lessons_by_group(group_name: str, db: Session):
    group_lessons = (
        db.query(Lesson)
        .filter(Lesson.group_name == group_name)
        .order_by(Lesson.first_group.desc())
        .all()
    )
    tmp_group_lessons = {
        "Monday": [[] for _ in range(6)],
        "Tuesday": [[] for _ in range(6)],
        "Wednesday": [[] for _ in range(6)],
        "Thursday": [[] for _ in range(6)],
        "Friday": [[] for _ in range(6)],
        "Saturday": [[] for _ in range(6)],
    }

    for lesson in group_lessons:
        day = lesson.day
        lesson_number = lesson.lesson_number
        print(lesson.day, lesson.lesson_title)
        tmp_group_lessons[get_day_display(day)][lesson_number].append(lesson)

    for days in tmp_group_lessons:
        print(days)
        for lessons_index in range(len(tmp_group_lessons[days])):
            lessons = tmp_group_lessons[days][lessons_index]
            if len(lessons) >= 2:
                tmp_group_lessons[days][lessons_index] = handle_combined_lessons(
                    lessons, "group"
                )
    return tmp_group_lessons


async def get_groups(db: Session, faculty=None):
    if faculty:
        lessons = (
            db.query(Lesson)
            .filter(Lesson.faculty == faculty)
            .order_by(Lesson.group_name)
            .all()
        )
    else:
        lessons = db.query(Lesson).order_by(Lesson.group_name).all()
    groups = [
        {"group_name": " ".join(lesson.group_name.split()), "faculty": lesson.faculty}
        for lesson in lessons
    ]
    groups = [dict(t) for t in {tuple(d.items()) for d in groups}]
    groups.sort(key=itemgetter("group_name"))
    # groups: list[str] = list(map(lambda g: ' '.join(
    #     [i for i in g.split(' ') if i != '']), groups))
    return groups


async def add_lesson(db: Session, lesson: LessonCreate, username: str) -> Lesson:
    tmp_lesson: Lesson = Lesson(**{"id": str(uuid4()), **lesson.model_dump()})
    log: Log = Log(
        **{
            "id": str(uuid4()),
            **lesson.model_dump(),
            "username": username,
            "action": "create",
            "date": datetime.datetime.now(),
        }
    )
    db.add(log)
    db.add(tmp_lesson)
    db.commit()
    db.refresh(tmp_lesson)
    db.refresh(log)
    return tmp_lesson


async def get_lessons(db: Session):
    return db.query(Lesson).all()


async def get_lessons_by_faculty(faculty: str, db: Session):
    return db.query(Lesson).filter(Lesson.faculty == faculty).all()


async def delete_lesson(db: Session, lesson_id: str, username: str):
    lesson = db.get(Lesson, lesson_id)
    lesson_data = PydanticLesson.model_validate(lesson).model_dump()
    lesson_data.pop("id")
    log: Log = Log(
        **{
            "id": str(uuid4()),
            **lesson_data,
            "username": username,
            "action": "delete",
            "date": datetime.datetime.now(),
        }
    )
    db.add(log)
    db.delete(lesson)
    db.commit()
    db.refresh(log)


async def delete_lessons_by_faculty(db: Session, faculty):
    db.query(Lesson).filter(Lesson.faculty == faculty).delete()
    db.commit()


async def edit_lesson(
    db: Session, lesson_id, updated_lesson: LessonCreate, username: str
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    update_data = updated_lesson.model_dump()
    log: Log = Log(
        **{
            "id": str(uuid4()),
            **updated_lesson.model_dump(),
            "username": username,
            "action": "edit",
        }
    )
    db.query(Lesson).filter(Lesson.id == lesson_id).update(
        update_data, synchronize_session=False
    )
    db.commit()
    db.refresh(lesson)
    db.refresh(log)
    return lesson
