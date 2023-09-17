def is_lessons_equal(first_lesson, second_lesson, compare):
    keys_to_compare = [
        "numerator",
        "denominator",
        "first_group",
        "second_group",
    ]
    if compare == "teacher":
        keys_to_compare.append("teacher_name")
    elif compare == "group":
        keys_to_compare.append("group_name")
    return all(first_lesson[key] == second_lesson[key] for key in keys_to_compare)
