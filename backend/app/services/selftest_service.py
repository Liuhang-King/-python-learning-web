"""自检业务逻辑：全量检查教程、练习题、判分与数据的完整性。

不修改任何数据，只读检查。返回结构化报告供前端「测试」页展示。
"""

from __future__ import annotations

from ..database import execute
from .exercise_service import answers_match

MIN_CONTENT_LENGTH = 100


def _issues() -> list[dict]:
    return []


def _add(issues: list[dict], level: str, category: str, name: str, detail: str) -> None:
    issues.append({"level": level, "category": category, "name": name, "detail": detail})


def run_selftest() -> dict:
    """执行一次全量自检，返回报告字典。"""
    issues: list[dict] = []

    # 1. 数据表与数量
    try:
        lesson_count = execute("SELECT COUNT(*) AS n FROM lessons").fetchone()["n"]
        exercise_count = execute("SELECT COUNT(*) AS n FROM exercises").fetchone()["n"]
    except Exception as exc:  # 表不存在等
        _add(issues, "error", "数据库", "表结构", f"无法读取数据：{type(exc).__name__}")
        return {
            "healthy": False,
            "summary": {"lessons": 0, "exercises": 0, "errors": 1, "warnings": 0, "checks": 1},
            "checks": [],
            "issues": issues,
        }

    checks: list[dict] = []

    # 2. 教程完整性
    bad_lessons = 0
    for row in execute("SELECT id, title, content_md, code_example FROM lessons ORDER BY order_index").fetchall():
        problems = []
        if not row["content_md"] or len(row["content_md"]) < MIN_CONTENT_LENGTH:
            problems.append("正文缺失或过短")
        if not row["code_example"] or not str(row["code_example"]).strip():
            problems.append("缺少示例代码")
        if not row["title"] or not str(row["title"]).strip():
            problems.append("标题为空")
        if problems:
            bad_lessons += 1
            for p in problems:
                _add(issues, "error", "教程", f"#{row['id']} {row['title'] or '(无标题)'}", p)
    checks.append({
        "name": "教程完整性",
        "total": lesson_count,
        "passed": lesson_count - bad_lessons,
        "ok": bad_lessons == 0,
    })

    # 3. order_index 连续性 + slug 唯一
    orders = [r["order_index"] for r in execute("SELECT order_index FROM lessons ORDER BY order_index").fetchall()]
    order_ok = orders == list(range(1, len(orders) + 1))
    if not order_ok:
        _add(issues, "warning", "教程", "排序编号", f"order_index 不连续：{orders[:10]}...")
    checks.append({"name": "教程排序连续", "total": 1, "passed": 1 if order_ok else 0, "ok": order_ok})

    duplicate_slugs = [r["slug"] for r in execute(
        "SELECT slug FROM lessons GROUP BY slug HAVING COUNT(*) > 1"
    ).fetchall()]
    if duplicate_slugs:
        _add(issues, "error", "教程", "slug 唯一性", f"重复 slug：{duplicate_slugs}")
    checks.append({
        "name": "教程 slug 唯一",
        "total": 1,
        "passed": 0 if duplicate_slugs else 1,
        "ok": not duplicate_slugs,
    })

    # 4. 练习题判分自测：用 expected_answer 反向提交，必须判对
    bad_exercises = 0
    rows = execute(
        "SELECT id, title, lesson_id, expected_answer, starter_code FROM exercises ORDER BY order_index"
    ).fetchall()
    for row in rows:
        problems = []
        answer = row["expected_answer"]
        if answer is None or not str(answer).strip():
            problems.append("答案为空")
        elif "\n" in str(answer).strip():
            problems.append("答案含多行（判分按单行文本比对）")
        elif not answers_match(answer, answer):
            problems.append("判分自测失败（答案无法匹配自身）")
        if row["lesson_id"] is None:
            problems.append("未关联教程")
        if problems:
            bad_exercises += 1
            for p in problems:
                _add(issues, "error", "练习题", f"#{row['id']} {row['title'] or '(无标题)'}", p)
    checks.append({
        "name": "练习题判分自测",
        "total": exercise_count,
        "passed": exercise_count - bad_exercises,
        "ok": bad_exercises == 0,
    })

    # 5. 每篇教程配套题目数 >= 1
    no_exercise_lessons = [r["id"] for r in execute(
        """SELECT l.id FROM lessons l
           LEFT JOIN exercises e ON e.lesson_id = l.id
           GROUP BY l.id HAVING COUNT(e.id) = 0"""
    ).fetchall()]
    if no_exercise_lessons:
        _add(issues, "warning", "教程", "配套练习", f"以下教程无练习题：{no_exercise_lessons}")
    checks.append({
        "name": "教程配套练习",
        "total": lesson_count,
        "passed": lesson_count - len(no_exercise_lessons),
        "ok": not no_exercise_lessons,
    })

    # 6. 数据库连通性
    try:
        execute("SELECT 1").fetchone()
        db_ok = True
    except Exception:
        db_ok = False
        _add(issues, "error", "数据库", "连通性", "SELECT 1 执行失败")
    checks.append({"name": "数据库连通", "total": 1, "passed": 1 if db_ok else 0, "ok": db_ok})

    errors = sum(1 for i in issues if i["level"] == "error")
    warnings = sum(1 for i in issues if i["level"] == "warning")

    return {
        "healthy": errors == 0,
        "summary": {
            "lessons": lesson_count,
            "exercises": exercise_count,
            "errors": errors,
            "warnings": warnings,
            "checks": len(checks),
        },
        "checks": checks,
        "issues": issues,
    }
