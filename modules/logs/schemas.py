from pydantic import BaseModel


class LogBase(BaseModel):
    username: str
    action: str
    lesson_title: str
    group_name: str
    teacher_name: str
    faculty: str
    lesson_type: str
    day: int
    lesson_number: int
    numerator: bool = False
    denominator: bool = False
    first_group: bool = False
    second_group: bool = False


class Log(LogBase):
    id: str

    class Config:
        from_attributes = True
