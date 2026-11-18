"""练习题控制器：只解析请求、调用 service、返回响应。"""

from __future__ import annotations

from flask import Blueprint, jsonify

from ..services import exercise_service
from ._helpers import get_json_body

exercises_bp = Blueprint("exercises", __name__, url_prefix="/api")


@exercises_bp.get("/exercises")
def list_exercises():
    return jsonify(exercise_service.get_exercise_summaries())


@exercises_bp.get("/exercises/<int:exercise_id>")
def get_exercise(exercise_id: int):
    return jsonify(exercise_service.get_exercise_detail(exercise_id))


@exercises_bp.post("/exercises/<int:exercise_id>/submit")
def submit(exercise_id: int):
    body = get_json_body()
    return jsonify(exercise_service.submit_code(exercise_id, body.get("code")))
