from pydantic import BaseModel


class TeacherBase(BaseModel):
    teacher_name: str
    faculty: str


class TeacherCreate(TeacherBase):
    pass


class Teacher(TeacherBase):
    id: str

    class Config:
        orm_mode = True
