from src.exceptions import NotFound, Conflict
from src.teachers.constants import ErrorCode


class TeacherNotFound(NotFound):
    DETAIL = ErrorCode.TEACHER_NOT_FOUND


class TeacherAlreadyExists(Conflict):
    DETAIL = ErrorCode.TEACHER_ALREADY_EXISTS
