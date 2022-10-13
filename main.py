"""Desribe of module"""
import os
from typing import List
from fastapi import Depends, FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from starlette.responses import HTMLResponse
import crud
import models
import schemas


from database import SessionLocal, engine
from excel_to_json import excel_to_json

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['http://localhost:3000', 'https://mspu-schedule.netlify.app', 'https://web.postman.co']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


FACULTIES = {'dino': 'ДиНО', 'fif': 'ФИФ',
             'ffk': 'ФФК', 'ff': 'ФФ', 'tbf': 'ТБФ'}


# Dependency
def get_db():
    """doc"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.delete('/teachers/{teacher_id}', status_code=204)
async def delete_teacher(teacher_id, db: Session=Depends(get_db)):
    return crud.delete_teacher(db, teacher_id)


@app.post('/teachers/add_teachers/')
async def add_teachers(teachers: List[schemas.TeacherCreate], db: Session=Depends(get_db)):
    return crud.add_teachers(db, teachers)

@app.post('/teachers/add_teacher/')
async def add_teacher(teacher: schemas.TeacherCreate, db: Session=Depends(get_db)):
    return crud.add_teacher(db, teacher)


@app.get('/upload_excel_schedule/', status_code=200)
async def upload_excel_schedule_form(faculty):
    """Generate HTML form for upload .xlsx file with schedule to server"""
    content = f"""
        <body>
        <p> {FACULTIES[faculty]} </p>
        <form action="/upload_excel_schedule/?faculty={faculty}" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit">
        </form>
        </form>
        </body>
    """
    return HTMLResponse(content=content)


@app.post('/upload_excel_schedule/', status_code=201)
async def upload_excel_schedule(faculty, file: UploadFile = File(...), db: Session = Depends(get_db)):
    with open(file.filename, 'wb+') as file_object:
        file_object.write(file.file.read())
    lessons = excel_to_json(file.filename)
    os.remove(file.filename)
    return crud.upload_excel_schedule(db, lessons, FACULTIES[faculty])


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
        result = crud.get_teachers_by_faculty(db, FACULTIES[faculty])
    elif not faculty:
        result = crud.get_teachers(db)
    return result


@app.get('/faculties/')
async def get_faculties():
    return

@app.post('/lessons')
async def add_lesson(lesson: Request, db=Depends(get_db)):
    lesson = await lesson.json() 
    return crud.add_lesson(db, lesson)

@app.put('/lessons/{lesson_id}')
async def edit_lesson(lesson_id, lesson: Request, db=Depends(get_db)):
    lesson = await lesson.json() 
    return crud.edit_lesson(db, lesson_id, lesson)

@app.delete('/lessons/{lesson_id}')
def delete_lesson(lesson_id, db=Depends(get_db)):
    return crud.delete_lesson(db, lesson_id)

@app.get('/delete_duplicate_teachers')
async def delete_duplicate_teachers(db=Depends(get_db)):
    return crud.delete_duplicate_teachers(db)
