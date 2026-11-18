"""学习进度数据访问层。

契约约定：一行记录表示一项完成，lesson_id 与 exercise_id 二选一非空。
由于 SQLite 的 UNIQUE 约束把 NULL 视为互不相等，这里使用带 NOT EXISTS 的
单条 INSERT 保证幂等（同一项重复标记不会产生重复行）。
"""

from __future__ import annotations

from datetime import datetime, timezone

from ..database import execute


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def list_completed_lesson_ids() -> list[int]:
    rows = execute(
        "SELECT lesson_id FROM progress WHERE lesson_id IS NOT NULL ORDER BY lesson_id ASC"
    ).fetchall()
    return [row["lesson_id"] for row in rows]


def list_completed_exercise_ids() -> list[int]:
    rows = execute(
        "SELECT exercise_id FROM progress WHERE exercise_id IS NOT NULL ORDER BY exercise_id ASC"
    ).fetchall()
    return [row["exercise_id"] for row in rows]


def count_lessons() -> int:
    return execute("SELECT COUNT(*) AS total FROM lessons").fetchone()["total"]


def count_exercises() -> int:
    return execute("SELECT COUNT(*) AS total FROM exercises").fetchone()["total"]


def mark_lesson_completed(lesson_id: int) -> bool:
    """返回 True 表示本次确实新增，False 表示此前已完成。"""
    cursor = execute(
        """
        INSERT INTO progress (lesson_id, exercise_id, completed_at)
        SELECT ?, NULL, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM progress WHERE lesson_id = ? AND exercise_id IS NULL
        )
        """,
        (lesson_id, _now(), lesson_id),
    )
    return cursor.rowcount > 0


def mark_exercise_completed(exercise_id: int) -> bool:
    """返回 True 表示本次确实新增，False 表示此前已完成。"""
    cursor = execute(
        """
        INSERT INTO progress (lesson_id, exercise_id, completed_at)
        SELECT NULL, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM progress WHERE exercise_id = ? AND lesson_id IS NULL
        )
        """,
        (exercise_id, _now(), exercise_id),
    )
    return cursor.rowcount > 0
