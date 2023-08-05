from modules.lessons.utils.is_teacher_lessons_equal import is_teacher_lessons_equal
from modules.lessons.models import Lesson


def combine_lessons(lesson_dicts):
    group_names = [lesson['group_name'] for lesson in lesson_dicts]
    lesson_ids = [lesson['id'] for lesson in lesson_dicts]
    common_lesson = lesson_dicts[0].copy()
    del common_lesson['id']
    del common_lesson['group_name']
    del common_lesson['_sa_instance_state']

    return Lesson(id=', '.join(lesson_ids), group_name=', '.join(group_names), **common_lesson)


def handle_combined_lessons(lessons):
    combined_lessons = []
    unique_teacher_lessons = []

    for lesson in lessons:
        lesson_dict = lesson.__dict__.copy()
        if any(is_teacher_lessons_equal(lesson_dict, unique_lesson) for unique_lesson in unique_teacher_lessons):
            unique_teacher_lessons.append(lesson_dict)
        else:
            if len(unique_teacher_lessons) >= 2:
                combined_lessons.append(combine_lessons(unique_teacher_lessons))
            unique_teacher_lessons = [lesson_dict]

    if len(unique_teacher_lessons) >= 2:
        combined_lessons.append(combine_lessons(unique_teacher_lessons))

    return combined_lessons
