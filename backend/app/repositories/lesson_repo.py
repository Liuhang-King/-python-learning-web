"""教程数据访问层。所有 SQL 均参数化。"""

from __future__ import annotations

from ..database import execute

_SUMMARY_COLUMNS = "id, slug, title, summary, order_index, duration_min"
_DETAIL_COLUMNS = (
    "id, slug, title, summary, content_md, code_example, order_index, duration_min"
)


def list_lessons() -> list[dict]:
    rows = execute(
        f"SELECT {_SUMMARY_COLUMNS} FROM lessons ORDER BY order_index ASC, id ASC"
    ).fetchall()
    return [dict(row) for row in rows]


def get_lesson(lesson_id: int) -> dict | None:
    row = execute(
        f"SELECT {_DETAIL_COLUMNS} FROM lessons WHERE id = ?", (lesson_id,)
    ).fetchone()
    return dict(row) if row is not None else None
