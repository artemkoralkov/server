from typing import Optional

from pydantic import BaseModel


class LessonBase(BaseModel):
    
    lesson_title: str
    group_name: str
    teacher_name: str
    faculty: str
    lesson_type: str
    day: int
    lesson_number: int
    numerator: Optional[bool] = False
    denominator: Optional[bool] = False
    first_group: Optional[bool] = False
    second_group: Optional[bool] = False


class LessonCreate(LessonBase):
    pass

class Lesson(LessonCreate):
    id: str

    class Config:
        orm_mode = True


class TeacherBase(BaseModel):
   
    teacher_name: str
    faculty: str


class TeacherCreate(TeacherBase):
    pass


class Teacher(TeacherBase):
    id: str
    class Config:
        orm_mode = True
