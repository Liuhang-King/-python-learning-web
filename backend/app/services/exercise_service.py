"""练习题业务逻辑：答案校验（不执行用户代码，安全优先）。"""

from __future__ import annotations

from ..errors import NotFoundError, ValidationError
from ..repositories import exercise_repo

# 统一各种引号为半角单引号：包括直双引号、中文弯引号、全角引号
_QUOTE_TRANSLATION = str.maketrans(
    {
        '"': "'",
        "“": "'",
        "”": "'",
        "‘": "'",
        "’": "'",
        "＂": "'",
        "＇": "'",
    }
)

_WRONG_HINT = (
    "再想想，参考提示：检查输出格式、引号写法与空格是否和题目要求一致。"
)


def normalize_answer(text: str) -> str:
    """去首尾空白 → 统一引号 → 忽略全部空白差异。"""
    return "".join(str(text).strip().translate(_QUOTE_TRANSLATION).split())


def answers_match(submitted: str, expected: str) -> bool:
    return normalize_answer(submitted) == normalize_answer(expected)


def get_exercise_summaries() -> list[dict]:
    return exercise_repo.list_exercises()


def get_exercise_detail(exercise_id: int) -> dict:
    exercise = exercise_repo.get_exercise(exercise_id)
    if exercise is None:
        raise NotFoundError("练习题不存在")
    return exercise


def submit_code(exercise_id: int, code: str) -> dict:
    if not isinstance(code, str) or not code.strip():
        raise ValidationError("提交内容 code 不能为空")

    expected = exercise_repo.get_expected_answer(exercise_id)
    if expected is None:
        raise NotFoundError("练习题不存在")

    if answers_match(code, expected):
        return {"correct": True, "message": "答对了！", "expected": expected}
    return {"correct": False, "message": _WRONG_HINT, "expected": None}
