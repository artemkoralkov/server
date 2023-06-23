
from uuid import uuid4
import requests


# files = {'file': open('E:/raspis_FIF__I_semestr_2021-2022.xlsx','rb')}

# url = 'http://127.0.0.1:8000/uploadfile/fif'
url = 'http://127.0.0.1:8000/teachers/'
print(requests.post(url, data={'teacher_name': 'test', 'faculty': 'test'}).text)


# lesson ='Безопасность жизнедеятельности человека (лк)+ФФ,ФФК доц. Николаенко Т.В.'
# lesson = lesson.replace('+', ' + ')
# lesson_split_by_plus = lesson.split(' + ')
# lesson_split_by_plus = list(map(lambda s: s.strip(), lesson_split_by_plus))
# lesson_name_and_lesson_type = lesson_split_by_plus[0]
# lesson_name = lesson_name_and_lesson_type.split('(')[0]
# lesson_type = lesson_name_and_lesson_type.split('(')[1].split(')')[0]
# lesson_teacher_and_faculty = lesson_split_by_plus[1]
# lesson_name =f'{lesson_name.strip()} + {lesson_teacher_and_faculty.split(" ")[0]}'
# lesson_teacher = ' '.join(lesson_teacher_and_faculty.split(' ')[1:])
# print(lesson_name)
# print(lesson_teacher)



teachers_fif = [
    "доц. Гуцко Н.В.",
    "доц. Ковальчук И.Н.",
    "доц. Сафанков Е.И.",
    "доц. Иваненко Л.А.",
    "доц. Давыдовская В.В.",
    "доц. Смолякова О.Ф.",
    "пр.-ст. Плюснин А.Г.",
    "ст.пр. Лешкевич М.Л.",
    "ст.пр. Макаренко А.В.",
    "ст.пр. Дубодел В.П.",
    "проф. Савенко В.С.",
    "ст.пр. Ефимчик И.А.",
    "проф. Кулак Г.В.",
    "ст.пр. Некрасова Г.Н.",
    "доц. Карпинская Т.В.",
    "пр.-ст. Коральков А.Д.",
    "ст.пр. Соболева Т.Г.",
    "доц. Бакланенко Л.Н.",
    "доц. Щур С.Н.",
    "доц. Голозубов А.Л.",
    "доц. Николаенко Т.В.",
    "доц. Мижуй С.М.",
    "пр.-ст. Зерница Д.А.",
    "ст.пр. Шутова Е.А.",
    "пр. Сливец О.Г.",
    "доц. Ефремова М.И.",
    "доц. Макаревич А.В.",
    "доц. Равуцкая Ж.И.",
    "доц. Овсиюк Е.М.",
    "доц. Голуб А.А.",
    "ст.пр. Игнатович С.В.",
    "доц. Бондарь С.Р.",
    "пр. Старовойтова О.В.",
    "доц. Гридюшко А.И.",
    "пр. Сафронов А.П."
]

teachers_dino = [
    "доц. Болбас Г.В.",
    "доц. Асташова А.Н.",
    "ст.пр. Пазняк Т.А.",
    "ст.пр. Стасилович Н.С.",
    "доц. Иванова Л.Н.",
    "доц. Жлудова Н.С.",
    "пр. Комонова А.В.",
    "доц. Журлова И.В.",
    "доц. Калач Л.А.",
    "доц. Борисенко Н.А..",
    "доц. Крук Б.А.",
    "ст.пр. Сливец О.Г.",
    "проф. Болбас В.С.",
    "доц.Ковалевская А.А.",
    "доц. Борисенко О.Е.",
    "ст.пр. Карпович И.А.",
    "доц. Солохов А.В.",
    "ст.пр. Злобина С.П.",
    "доц. Исмайлова Л.В.",
    "ст.пр. Михайлова Е.Н.",
    "ст.пр.Михайлова",
    "ст.пр. Карпович И.А.",
    "пр. Кузьменко Е.В.",
    "ст.пр.Стасилович Н.С.",
    "ст.пр. Малашенко В.В.",
    "доц. Лисовский Л.А.",
    "доц. Кошман П.Г.",
    "доц Цырулик Н.С.",
]

teachers= [{'id': str(uuid4()), 'teacher_name': i, 'faculty': 'ДиНО'} for i in teachers_dino]
# teacher = {'day': 0,
# 'denominator': False,
# "faculty": "ФИФ",
# 'first_group': False,
# 'group_name': "1/1 Матем. и информ.",
# 'lesson_number': 0,
# 'lesson_title': "213123",
# 'lesson_type': "лк",
# 'numerator': False,
# 'second_group': False,
# 'teacher_name': "пр.-ст. Коральков А.Д."}
# teachers= [{'teacher_name': "ст.пр. Варнава З.С.", 'faculty': 'ФИФ'}, {'teacher_name': "доц. Телепень С.В.", 'faculty': 'ФИФ'}]
# teacher = {'id': str(uuid4()), 'teacher_name': 'пр.-ст. Коральков А.Д.', 'faculty': 'ФИФ'}
# print(teacher)
# r = requests.post(url, json=teachers)
# print(r.text)

FACULTIES = {'fif': 'ФИФ', 'ffk': 'ФФК', 'ff': 'ФФ', 'tbf': 'ТБФ', 'dino': 'ДиНО'}
# print(list(FACULTIES.values()))

# for group in result:
#     i = 1
#     for days in result[group]:
#         for lessons_indx in range(len(days)):
#             if type(days[lessons_indx]) is list:
                
#                 for lesson in days[lessons_indx]:
#                     numerator = 'numerator' in lesson
#                     denominator = 'denominator' in lesson
#                     first_group = 'first_group' in lesson
#                     second_group = 'second_group' in lesson
#                     if 'lesson_type' in lesson:
#                         lesson_type = lesson['lesson_type']
#                     else:
#                         lesson_type = ''
#                     if 'lesson' in lesson:
#                         continue
#                     create_lesson({'lesson_name': lesson['lesson_name'],
#                                     'group_name': group,
#                                     'teacher_name': lesson['lesson_teacher'],
#                                     'lesson_type': lesson_type,
#                                     'faculty': 'ФФ',
#                                     'lesson_number': lessons_indx,
#                                     'day': i,
#                                     'numerator': numerator,
#                                     'denominator': denominator,
#                                     'first_group': first_group,
#                                     'second_group': second_group
#                                     })
#             else:
#                 if 'lesson' in days[lessons_indx]:
#                     continue
#                 if 'lesson_type' in days[lessons_indx]:
#                         lesson_type = days[lessons_indx]['lesson_type']
#                 else:
#                         lesson_type = ''
#                 create_lesson({'lesson_name': days[lessons_indx]['lesson_name'],
#                                     'group_name': group,
#                                     'teacher_name': days[lessons_indx]['lesson_teacher'],
#                                     'lesson_type': lesson_type,
#                                     'faculty': 'ФФ',
#                                     'lesson_number': lessons_indx,
#                                     'day': i
#                                     })
#         i += 1    
                

# for lesson_index in range(len(group)):
#     print(lesson_index)
#     if type(result[group[lesson_index]]) is list:
#         for k in result[group[lesson_index]]:
#             numerator = 'numerator' in result[group[lesson_index]]
#             denominator = 'denominator' in result[group[lesson_index]]
#             first_group = 'first_group' in result[group[lesson_index]]
#             second_group = 'second_group' in result[group[lesson_index]]
#             if 'lesson_type' in result[group[lesson_index]]:
#                 lesson_type = result[group[lesson_index]]['lesson_type']
#             else:
#                 lesson_type = ''
#             print({'lesson_name': k.lesson_name,
#                                     'group_name': group,
#                                     'teacher_name': k.lesson_teacher,
#                                     'lesson_type': lesson_type,
#                                     'faculty': 'ФФ',
#                                     'day': lesson_index,
#                                     'numerator': numerator,
#                                     'denominator': denominator,
#                                     'first_group': first_group,
#                                     'second_group': second_group
#                                     })
