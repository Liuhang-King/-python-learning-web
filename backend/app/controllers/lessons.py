"""教程控制器：只解析请求、调用 service、返回响应。"""

from __future__ import annotations

from flask import Blueprint, jsonify

from ..services import lesson_service

lessons_bp = Blueprint("lessons", __name__, url_prefix="/api")


@lessons_bp.get("/lessons")
def list_lessons():
    return jsonify(lesson_service.get_lesson_summaries())


@lessons_bp.get("/lessons/<int:lesson_id>")
def get_lesson(lesson_id: int):
    return jsonify(lesson_service.get_lesson_detail(lesson_id))
