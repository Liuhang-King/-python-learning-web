"""练习题数据访问层。

注意：expected_answer 只通过 get_expected_answer() 供校验使用，
绝不出现在任何对外返回的详情字典中。
"""

from __future__ import annotations

from ..database import execute

_SUMMARY_COLUMNS = "id, lesson_id, title, difficulty, order_index"
_DETAIL_COLUMNS = (
    "id, lesson_id, title, description, starter_code, difficulty, order_index"
)


def list_exercises() -> list[dict]:
    rows = execute(
        f"SELECT {_SUMMARY_COLUMNS} FROM exercises ORDER BY order_index ASC, id ASC"
    ).fetchall()
    return [dict(row) for row in rows]


def get_exercise(exercise_id: int) -> dict | None:
    row = execute(
        f"SELECT {_DETAIL_COLUMNS} FROM exercises WHERE id = ?", (exercise_id,)
    ).fetchone()
    return dict(row) if row is not None else None


def get_expected_answer(exercise_id: int) -> str | None:
    row = execute(
        "SELECT expected_answer FROM exercises WHERE id = ?", (exercise_id,)
    ).fetchone()
    return None if row is None else row["expected_answer"]


def list_exercise_ids_by_lesson(lesson_id: int) -> list[int]:
    rows = execute(
        "SELECT id FROM exercises WHERE lesson_id = ? ORDER BY order_index ASC, id ASC",
        (lesson_id,),
    ).fetchall()
    return [row["id"] for row in rows]
