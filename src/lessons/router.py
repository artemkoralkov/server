from pathlib import Path

from fastapi import Depends, UploadFile, File, Request, APIRouter, status, Header, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import src.lessons.service as crud
from src.constants import FACULTIES
from src.database import get_db
from src.lessons.schemas import LessonCreate

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))

lessons_router = APIRouter(prefix="/lessons", tags=["lessons"])


@lessons_router.get("", status_code=status.HTTP_200_OK)
async def get_lessons(
    faculty="", group_name="", teacher_name="", db: Session = Depends(get_db)
):
    if faculty:
        result = await crud.get_lessons_by_faculty(FACULTIES[faculty], db)
    elif group_name:
        result = await crud.get_lessons_by_group(group_name, db)
    elif teacher_name:
        result = await crud.get_lessons_by_teacher(teacher_name, db)
    else:
        result = await crud.get_lessons(db)
    return result


@lessons_router.get("/upload_excel_schedule", status_code=status.HTTP_200_OK)
async def upload_excel_schedule_form(request: Request):
    """Generate HTML form for upload .xlsx file with schedule to server"""
    return templates.TemplateResponse(
        "upload_excel_form.html",
        {
            "request": request,
            "faculties": FACULTIES,
        },
    )


@lessons_router.get("/groups", status_code=status.HTTP_200_OK)
async def get_groups(faculty="", db: Session = Depends(get_db)):
    if faculty:
        return await crud.get_groups(db, FACULTIES[faculty])
    return await crud.get_groups(db)


@lessons_router.post("/upload_excel_schedule", status_code=status.HTTP_201_CREATED)
async def upload_excel_schedule(
    faculty: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return await crud.upload_excel_schedule(db, file, FACULTIES[faculty])


@lessons_router.post("", status_code=status.HTTP_201_CREATED)
async def add_lesson(
    lesson: LessonCreate, username: str = Header(), db=Depends(get_db)
):
    return await crud.add_lesson(db, lesson, username)


@lessons_router.put("/{lesson_id}", status_code=status.HTTP_200_OK)
async def edit_lesson(
    lesson_id, edited_lesson: LessonCreate, username: str = Header(), db=Depends(get_db)
):
    # lesson: dict[str, str] = await incoming_lesson.json()
    return await crud.edit_lesson(db, lesson_id, edited_lesson, username)


@lessons_router.delete("/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lesson(lesson_id, username: str = Header(), db=Depends(get_db)):
    return await crud.delete_lesson(db, lesson_id, username)


@lessons_router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lessons(faculty, db=Depends(get_db)):
    await crud.delete_lessons_by_faculty(db, FACULTIES[faculty])
