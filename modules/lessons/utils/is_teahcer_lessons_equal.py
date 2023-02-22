def is_teahcer_lessons_equal(first_lesson, second_lesson):
    return first_lesson['numerator'] == second_lesson['numerator'] and \
        first_lesson['denominator'] == second_lesson['denominator'] and \
        first_lesson['faculty'] == second_lesson['faculty'] and \
        first_lesson['denominator'] == second_lesson['denominator'] and \
        first_lesson['teacher_name'] == second_lesson['teacher_name'] and \
        first_lesson['first_group'] == second_lesson['first_group'] and \
        first_lesson['second_group'] == second_lesson['second_group']
