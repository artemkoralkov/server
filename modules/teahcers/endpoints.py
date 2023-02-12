from typing import List
from fastapi import Depends, Request, Form, HTTPException, APIRouter

from fastapi.templating import Jinja2Templates

from .crud import *
from .schemas import *

from deps import get_db


templates = Jinja2Templates(directory='./templates')

FACULTIES: dict[str, str] = {'dino': 'ДиНО', 'fif': 'ФИФ',
                             'ffk': 'ФФК', 'ff': 'ФФ', 'tbf': 'ТБФ'}

teachers_router = APIRouter(
    prefix='/teachers',
    tags=['teachers']
)


@teachers_router.delete('/{teacher_id}', status_code=204)
async def delete_teacher(teacher_id, db: Session = Depends(get_db)):
    return delete_teacher(db, teacher_id)


@teachers_router.post('/add_teachers', response_model=list[Teacher])
async def add_teachers(teachers: List[TeacherCreate], db: Session = Depends(get_db)):
    return add_teachers(db, teachers)


@teachers_router.get('/add_teacher')
async def add_teacher(request: Request):
    return templates.TemplateResponse(
        'add_teacher_form.html',
        {
            'request': request,
            'faculties': list(FACULTIES.values())
        }
    )


@teachers_router.post('/add_teacher')
async def add_teacher(
        request: Request, teacher_name: str = Form(...), faculty: str = Form(...), db: Session = Depends(get_db)
):
    db_teacher = get_teacher_by_name(db, teacher_name)
    if db_teacher:
        raise HTTPException(status_code=400, detail="Teacher is already exist")

    teacher: TeacherCreate = TeacherCreate(teacher_name=teacher_name, faculty=faculty)
    return add_teacher(db, teacher)


@teachers_router.get('/')
async def get_teachers(faculty='', db=Depends(get_db)):
    if faculty:
        return get_teachers_by_faculty(db, FACULTIES[faculty])
    elif not faculty:
        return get_teachers(db)


@teachers_router.get('/delete_duplicate_teachers')
async def delete_duplicate_teachers(db=Depends(get_db)):
    return delete_duplicate_teachers(db)
