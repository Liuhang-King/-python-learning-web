"""学习进度控制器：只解析请求、调用 service、返回响应。"""

from __future__ import annotations

from flask import Blueprint, jsonify

from ..services import progress_service
from ._helpers import get_json_body

progress_bp = Blueprint("progress", __name__, url_prefix="/api")


@progress_bp.get("/progress")
def get_progress():
    return jsonify(progress_service.get_summary())


@progress_bp.post("/progress/lessons/<int:lesson_id>")
def complete_lesson(lesson_id: int):
    return jsonify(progress_service.complete_lesson(lesson_id))


@progress_bp.post("/progress/exercises/<int:exercise_id>")
def complete_exercise(exercise_id: int):
    body = get_json_body()
    return jsonify(
        progress_service.complete_exercise(exercise_id, body.get("correct"))
    )
