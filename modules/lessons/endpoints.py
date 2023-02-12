import os
from fastapi import Depends, UploadFile, File, Request, APIRouter
from fastapi.templating import Jinja2Templates

from .crud import *
from .schemas import *

from modules.lessons.excel_to_json import excel_to_json
from deps import get_db

templates = Jinja2Templates(directory='./templates')

FACULTIES: dict[str, str] = {'dino': 'ДиНО', 'fif': 'ФИФ',
                             'ffk': 'ФФК', 'ff': 'ФФ', 'tbf': 'ТБФ'}

lessons_router = APIRouter(
    prefix='/lessons',
    tags=['lessons']
)


@lessons_router.get('/upload_excel_schedule', status_code=200)
async def upload_excel_schedule_form(request: Request, faculty):
    """Generate HTML form for upload .xlsx file with schedule to server"""
    return templates.TemplateResponse(
        'upload_excel_form.html',
        {
            'request': request,
            'faculties': FACULTIES,
            'faculty': faculty,
        }
    )


@lessons_router.post('/upload_excel_schedule', status_code=201)
async def upload_excel_schedule(faculty, file: UploadFile = File(...), db: Session = Depends(get_db)):
    with open(f'{file.filename}', 'wb+') as file_object:
        file_object.write(file.file.read())
    schedule = excel_to_json(f'{file.filename}')
    os.remove(f'{file.filename}')
    return upload_excel_schedule(db, schedule, FACULTIES[faculty])


@lessons_router.get('/', status_code=200)
async def get_lessons(group_name='', teacher_name='', db: Session = Depends(get_db)):
    if group_name:
        result = get_lessons_by_group(db, group_name)
    elif teacher_name:
        result = get_lessons_by_teacher(teacher_name, db)
    else:
        result = get_lessons(db)
    return result


@lessons_router.get('/groups')
async def get_groups_by_faculty(faculty='', db: Session = Depends(get_db)):
    if faculty:
        return get_groups_by_faculty(FACULTIES[faculty], db)
    return get_groups(db)


@lessons_router.post('/')
async def add_lesson(json_lesson: Request, db=Depends(get_db)):
    lesson: LessonCreate = await json_lesson.json()
    return add_lesson(db, lesson)


@lessons_router.put('/{lesson_id}')
async def edit_lesson(lesson_id, incoming_lesson: Request, db=Depends(get_db)):
    lesson: dict[str, str] = await incoming_lesson.json()
    return edit_lesson(db, lesson_id, lesson)


@lessons_router.delete('/{lesson_id}')
def delete_lesson(lesson_id, db=Depends(get_db)):
    return delete_lesson(db, lesson_id)
