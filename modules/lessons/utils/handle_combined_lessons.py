from .is_teahcer_lessons_equal import is_teahcer_lessons_equal
from ..models import Lesson

def handle_combined_lessons(lessons):
    if len(lessons) == 2:
        first_lesson_dict = lessons[0].__dict__
        second_lesson_dict = lessons[1].__dict__
        if is_teahcer_lessons_equal(first_lesson_dict, second_lesson_dict):
            group = f'{first_lesson_dict["group_name"]}, {second_lesson_dict["group_name"]}'
            lesson_id = f'{first_lesson_dict["id"]}, {second_lesson_dict["id"]}'
            del first_lesson_dict["id"]
            del first_lesson_dict['group_name']
            del first_lesson_dict['_sa_instance_state']
            return [Lesson(id=lesson_id, group_name=group, **first_lesson_dict)]
        else:
            return lessons
    elif len(lessons) == 3:
        first_lesson_dict = lessons[0].__dict__
        second_lesson_dict = lessons[1].__dict__
        third_lesson_dict = lessons[2].__dict__
        if is_teahcer_lessons_equal(first_lesson_dict, second_lesson_dict) and not is_teahcer_lessons_equal(first_lesson_dict, third_lesson_dict):
            if first_lesson_dict["group_name"][:3] + first_lesson_dict["group_name"][5:] == second_lesson_dict["group_name"][:3] + second_lesson_dict["group_name"][5:]:
                group = first_lesson_dict["group_name"][:3] + first_lesson_dict["group_name"][5:]
            else:
                group = f'{first_lesson_dict["group_name"]}, {second_lesson_dict["group_name"]}'
            lesson_id = f'{first_lesson_dict["id"]}, {second_lesson_dict["id"]}'
            del first_lesson_dict["id"]
            del first_lesson_dict['group_name']
            del first_lesson_dict['_sa_instance_state']
            del third_lesson_dict['_sa_instance_state']
            return [Lesson(id=lesson_id, group_name=group, **first_lesson_dict), Lesson(**third_lesson_dict)]
        elif is_teahcer_lessons_equal(first_lesson_dict, third_lesson_dict) and not is_teahcer_lessons_equal(first_lesson_dict, second_lesson_dict):
            if first_lesson_dict["group_name"][:3] + first_lesson_dict["group_name"][5:] == \
             third_lesson_dict["group_name"][:3] + third_lesson_dict["group_name"][5:]:
                group = first_lesson_dict["group_name"][:3] + first_lesson_dict["group_name"][5:]
            else:
                group = f'{first_lesson_dict["group_name"]}, {third_lesson_dict["group_name"]}'
            lesson_id = f'{first_lesson_dict["id"]}, {third_lesson_dict["id"]}'
            del first_lesson_dict["id"]
            del first_lesson_dict['group_name']
            del first_lesson_dict['_sa_instance_state']
            del second_lesson_dict['_sa_instance_state']
            return [Lesson(id=lesson_id, group_name=group, **first_lesson_dict), Lesson(**second_lesson_dict)]
        elif is_teahcer_lessons_equal(second_lesson_dict, third_lesson_dict) and not is_teahcer_lessons_equal(first_lesson_dict, second_lesson_dict):
            if second_lesson_dict["group_name"][:3] + second_lesson_dict["group_name"][5:] == \
             third_lesson_dict["group_name"][:3] + third_lesson_dict["group_name"][5:]:
                group = second_lesson_dict["group_name"][:3] + first_lesson_dict["group_name"][5:]
            else:
                group = f'{second_lesson_dict["group_name"]}, {third_lesson_dict["group_name"]}'
            lesson_id = f'{second_lesson_dict["id"]}, {third_lesson_dict["id"]}'
            del second_lesson_dict["id"]
            del second_lesson_dict['group_name']
            del second_lesson_dict['_sa_instance_state']
            del first_lesson_dict['_sa_instance_state']
            return [Lesson(id=lesson_id, group_name=group, **second_lesson_dict), Lesson(**first_lesson_dict)]
        elif is_teahcer_lessons_equal(first_lesson_dict, second_lesson_dict) and is_teahcer_lessons_equal(first_lesson_dict, third_lesson_dict):
            group = f'{first_lesson_dict["group_name"]}, {second_lesson_dict["group_name"]}, {third_lesson_dict["group_name"]}'
            lesson_id = f'{first_lesson_dict["group_name"]}, {second_lesson_dict["id"]}, {third_lesson_dict["id"]}'
            del first_lesson_dict["id"]
            del first_lesson_dict['group_name']
            del first_lesson_dict['_sa_instance_state']
            return [Lesson(id=lesson_id, group_name=group, **second_lesson_dict)]
        else:
            return lessons
 
        
