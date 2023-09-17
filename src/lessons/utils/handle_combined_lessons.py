from src.lessons.utils.is_lessons_equal import is_lessons_equal
from src.lessons.models import Lesson


def combine_lessons(lesson_dicts, compare):
    group_names = [lesson["group_name"] for lesson in lesson_dicts]
    teacher_names = [lesson["teacher_name"] for lesson in lesson_dicts]
    print(teacher_names)
    lesson_ids = [lesson["id"] for lesson in lesson_dicts]
    common_lesson = lesson_dicts[0].copy()
    del common_lesson["id"]
    if compare == 'teacher':
        del common_lesson["group_name"]
        return Lesson(
            id=", ".join(lesson_ids), group_name=", ".join(group_names), **common_lesson
        )
    elif compare == 'group':
        del common_lesson["teacher_name"]
        return Lesson(
            id=", ".join(lesson_ids), teacher_name=", ".join(teacher_names), **common_lesson
        )


def handle_combined_lessons(lessons, compare):
    combined_lessons = []
    unique_lessons = []
    for lesson in lessons:
        lesson_dict = lesson.__dict__.copy()
        if "_sa_instance_state" in lesson_dict:
            del lesson_dict["_sa_instance_state"]
        if any(
            is_lessons_equal(lesson_dict, unique_lesson, compare)
            for unique_lesson in unique_lessons
        ):
            unique_lessons.append(lesson_dict)
        else:
            if len(unique_lessons) >= 2:
                combined_lessons.append(combine_lessons(unique_lessons, compare))
            else:
                combined_lessons.extend(
                    [Lesson(**lesson) for lesson in unique_lessons]
                )
            unique_lessons = [lesson_dict]

    if len(unique_lessons) >= 2:
        combined_lessons.append(combine_lessons(unique_lessons, compare))
    else:
        combined_lessons.extend([Lesson(**lesson) for lesson in unique_lessons])

    return combined_lessons
