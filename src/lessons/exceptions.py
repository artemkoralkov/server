from src.exceptions import NotFound
from src.lessons.constants import ErrorCode


class LessonNotFound(NotFound):
    DETAIL = ErrorCode.LESSON_NOT_FOUND
