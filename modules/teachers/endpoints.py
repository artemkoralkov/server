from typing import List
from fastapi import Depends, Request, Form, HTTPException, APIRouter, status

from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from modules.teachers.schemas import *
import modules.teachers.crud as crud

from database import get_db
from constants import FACULTIES

templates = Jinja2Templates(directory='./templates')

teachers_router = APIRouter(
    prefix='/teachers',
    tags=['teachers']
)


@teachers_router.get('')
async def get_teachers(faculty='', db=Depends(get_db)):
    if faculty:
        return await crud.get_teachers_by_faculty(db, FACULTIES[faculty])
    elif not faculty:
        return await crud.get_teachers(db)


# @teachers_router.get('/delete_duplicate_teachers')
# async def delete_duplicate_teachers(db=Depends(get_db)):
#     return await crud.delete_duplicate_teachers(db)


@teachers_router.get('/add_teacher')
async def get_add_teacher_form(request: Request):
    return templates.TemplateResponse(
        'add_teacher_form.html',
        {
            'request': request,
            'faculties': list(FACULTIES.values())
        }
    )


@teachers_router.post('/add_teacher', status_code=status.HTTP_201_CREATED)
async def add_teacher(
        request: Request, teacher_name: str = Form(...), faculty: str = Form(...), db: Session = Depends(get_db)
):
    db_teacher = await crud.get_teacher_by_name(db, teacher_name)
    if db_teacher:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Teacher is already exist')

    teacher: TeacherCreate = TeacherCreate(teacher_name=teacher_name, faculty=faculty)
    return await crud.add_teacher(db, teacher)


@teachers_router.post('/add_teachers', status_code=status.HTTP_201_CREATED)
async def add_teachers(teachers: List[TeacherCreate], db: Session = Depends(get_db)):
    return await crud.add_teachers(db, teachers)


@teachers_router.delete('/{teacher_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher(teacher_id, db: Session = Depends(get_db)):
    return await crud.delete_teacher(db, teacher_id)
