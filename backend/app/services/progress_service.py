"""学习进度业务逻辑：汇总统计与完成标记。"""

from __future__ import annotations

from ..errors import NotFoundError, ValidationError
from ..repositories import exercise_repo, lesson_repo, progress_repo


def get_summary() -> dict:
    completed_lesson_ids = progress_repo.list_completed_lesson_ids()
    completed_exercise_ids = progress_repo.list_completed_exercise_ids()
    total_lessons = progress_repo.count_lessons()
    total_exercises = progress_repo.count_exercises()

    total_units = total_lessons + total_exercises
    completed_units = len(completed_lesson_ids) + len(completed_exercise_ids)
    percent = (
        min(100, max(0, round(completed_units / total_units * 100)))
        if total_units
        else 0
    )

    return {
        "completed_lesson_ids": completed_lesson_ids,
        "completed_exercise_ids": completed_exercise_ids,
        "total_lessons": total_lessons,
        "total_exercises": total_exercises,
        "completion_percent": percent,
    }


def complete_lesson(lesson_id: int) -> dict:
    if lesson_repo.get_lesson(lesson_id) is None:
        raise NotFoundError("教程不存在")
    progress_repo.mark_lesson_completed(lesson_id)
    return {"id": lesson_id, "completed": True}


def complete_exercise(exercise_id: int, correct: object) -> dict:
    if not isinstance(correct, bool):
        raise ValidationError("correct 必须是布尔值")

    if exercise_repo.get_exercise(exercise_id) is None:
        raise NotFoundError("练习题不存在")

    if correct:
        progress_repo.mark_exercise_completed(exercise_id)
    return {"id": exercise_id, "completed": correct}
