from pydantic import BaseModel


class LessonBase(BaseModel):
    lesson_title: str
    group_name: str
    teacher_name: str
    faculty: str
    lesson_type: str
    day: int
    lesson_number: int
    numerator: bool = False
    denominator:bool = False
    first_group: bool = False
    second_group: bool = False


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
