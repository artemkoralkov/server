import os
from typing import List, Literal
from fastapi import Depends, FastAPI, UploadFile, File, Request, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

import crud
import models
import schemas

from database import SessionLocal, engine
from excel_to_json import excel_to_json

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory='./templates')
app = FastAPI()
# drive = Drive('simple_drive')

origins: list[str] = ['http://localhost:3000',
                      'https://mspu-schedule.netlify.app', 'https://web.postman.co']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

FACULTIES: dict[str, str] = {'dino': 'ДиНО', 'fif': 'ФИФ',
                             'ffk': 'ФФК', 'ff': 'ФФ', 'tbf': 'ТБФ'}


# Dependency
def get_db():
    """doc"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'os': os.listdir('../../..')
         }
    )


@app.delete('/teachers/{teacher_id}', status_code=204)
async def delete_teacher(teacher_id, db: Session = Depends(get_db)):
    return crud.delete_teacher(db, teacher_id)


@app.post('/teachers/add_teachers/', response_model=list[schemas.Teacher])
async def add_teachers(teachers: List[schemas.TeacherCreate], db: Session = Depends(get_db)):
    return crud.add_teachers(db, teachers)


@app.get('/teachers/add_teacher')
async def add_teacher(request: Request):
    return templates.TemplateResponse(
        'add_teacher_form.html',
        {
            'request': request,
            'faculties': list(FACULTIES.values())
        }
    )


@app.post('/teachers/add_teacher')
async def add_teacher(
        request: Request, teacher_name: str = Form(...), faculty: str = Form(...), db: Session = Depends(get_db)
):
    db_teacher = crud.get_teacher_by_name(db, teacher_name)
    if db_teacher:
        raise HTTPException(status_code=400, detail="Teacher is already exist")

    teacher: schemas.TeacherCreate = schemas.TeacherCreate(teacher_name=teacher_name, faculty=faculty)
    return crud.add_teacher(db, teacher)


@app.get('/upload_excel_schedule/', status_code=200)
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


@app.post('/upload_excel_schedule/', status_code=201)
async def upload_excel_schedule(faculty, file: UploadFile = File(...), db: Session = Depends(get_db)):
    with open(f'../tmp/{file.filename}', 'wb+') as file_object:
        file_object.write(file.file.read())
    schedule = excel_to_json(f'../tmp/{file.filename}')
    os.remove(f'../tmp/{file.filename}')
    return crud.upload_excel_schedule(db, schedule, FACULTIES[faculty])


@app.get('/lessons/', status_code=200)
async def get_lessons(group_name='', teacher_name='', db: Session = Depends(get_db)):
    if group_name:
        result = crud.get_lessons_by_group(db, group_name)
    elif teacher_name:
        result = crud.get_lessons_by_teacher(teacher_name, db)
    else:
        result = crud.get_lessons(db)
    return result


@app.get('/groups/')
async def get_groups_by_faculty(faculty='', db: Session = Depends(get_db)):
    if faculty:
        return crud.get_groups_by_faculty(FACULTIES[faculty], db)
    return crud.get_groups(db)


@app.get('/teachers/')
async def get_teachers(faculty='', db=Depends(get_db)):
    if faculty:
        return crud.get_teachers_by_faculty(db, FACULTIES[faculty])
    elif not faculty:
        return crud.get_teachers(db)


@app.get('/faculties/')
async def get_faculties():
    return


@app.post('/lessons')
async def add_lesson(json_lesson: Request, db=Depends(get_db)):
    lesson: schemas.LessonCreate = await json_lesson.json()
    return crud.add_lesson(db, lesson)


@app.put('/lessons/{lesson_id}')
async def edit_lesson(lesson_id, incoming_lesson: Request, db=Depends(get_db)):
    lesson: dict[str, str] = await incoming_lesson.json()
    return crud.edit_lesson(db, lesson_id, lesson)


@app.delete('/lessons/{lesson_id}')
def delete_lesson(lesson_id, db=Depends(get_db)):
    return crud.delete_lesson(db, lesson_id)


@app.get('/delete_duplicate_teachers')
async def delete_duplicate_teachers(db=Depends(get_db)):
    return crud.delete_duplicate_teachers(db)
