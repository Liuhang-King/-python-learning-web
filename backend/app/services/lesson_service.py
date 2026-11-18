"""教程业务逻辑。本模块不导入 flask，不依赖任何请求对象。"""

from __future__ import annotations

from ..errors import NotFoundError
from ..repositories import exercise_repo, lesson_repo


def get_lesson_summaries() -> list[dict]:
    return lesson_repo.list_lessons()


def get_lesson_detail(lesson_id: int) -> dict:
    lesson = lesson_repo.get_lesson(lesson_id)
    if lesson is None:
        raise NotFoundError("教程不存在")
    lesson["exercise_ids"] = exercise_repo.list_exercise_ids_by_lesson(lesson_id)
    return lesson
