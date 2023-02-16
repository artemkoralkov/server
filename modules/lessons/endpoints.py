import os
from fastapi import Depends, UploadFile, File, Request, APIRouter, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .schemas import *

from modules.lessons.utils.excel_to_json import excel_to_json
import modules.lessons.crud as crud
from database import get_db

templates = Jinja2Templates(directory='./templates')

FACULTIES: 'dict[str, str]' = {'dino': 'ДиНО', 'fif': 'ФИФ',
                             'ffk': 'ФФК', 'ff': 'ФФ', 'tbfb': 'ТБФ(б)', 'tbft': 'ТБФ(т)'}

lessons_router = APIRouter(
    prefix='/lessons',
    tags=['lessons']
)


@lessons_router.get('/', status_code=status.HTTP_200_OK)
async def get_lessons(group_name='', teacher_name='', db: Session = Depends(get_db)):
    if group_name:
        result = await crud.get_lessons_by_group(group_name, db)
    elif teacher_name:
        result = await crud.get_lessons_by_teacher(teacher_name, db)
    else:
        result = await crud.get_lessons(db)
    return result


@lessons_router.get('/upload_excel_schedule', status_code=status.HTTP_200_OK)
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


@lessons_router.get('/groups', status_code=status.HTTP_200_OK)
async def get_groups(faculty='', db: Session = Depends(get_db)):
    if faculty:
        return await crud.get_groups_by_faculty(FACULTIES[faculty], db)
    return await crud.get_groups(db)


@lessons_router.post('/upload_excel_schedule', status_code=status.HTTP_201_CREATED)
async def upload_excel_schedule(faculty, file: UploadFile = File(...), db: Session = Depends(get_db)):
    with open(f'{file.filename}', 'wb+') as file_object:
        file_object.write(file.file.read())
    schedule = excel_to_json(f'{file.filename}', faculty)
    os.remove(f'{file.filename}')
    return await crud.upload_excel_schedule(db, schedule, FACULTIES[faculty])


@lessons_router.post('/', status_code=status.HTTP_201_CREATED)
async def add_lesson(json_lesson: Request, db=Depends(get_db)):
    lesson: LessonCreate = await json_lesson.json()
    return await crud.add_lesson(db, lesson)


@lessons_router.put('/{lesson_id}', status_code=status.HTTP_200_OK)
async def edit_lesson(lesson_id, incoming_lesson: Request, db=Depends(get_db)):
    lesson: dict[str, str] = await incoming_lesson.json()
    return await crud.edit_lesson(db, lesson_id, lesson)


@lessons_router.delete('/{lesson_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_lesson(lesson_id, db=Depends(get_db)):
    return await crud.delete_lesson(db, lesson_id)
