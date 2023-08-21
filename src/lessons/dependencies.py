from typing import Mapping

from src.lessons import service
from src.lessons.exceptions import LessonNotFound


async def valid_lesson_id(lesson_id: str) -> Mapping:
    lesson = await service.get_lesson_by_id(lesson_id)
    if not lesson:
        raise LessonNotFound()
    return lesson
