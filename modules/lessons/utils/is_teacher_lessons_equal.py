def is_teacher_lessons_equal(first_lesson, second_lesson):
    keys_to_compare = ['numerator', 'denominator', 'teacher_name', 'first_group', 'second_group']
    return all(first_lesson[key] == second_lesson[key] for key in keys_to_compare)
