"""健康检查控制器。"""

from __future__ import annotations

from flask import Blueprint, jsonify

from ..database import get_db

health_bp = Blueprint("health", __name__, url_prefix="/api")


@health_bp.get("/health")
def health():
    return jsonify({"status": "ok", "service": "python-learning-web"})


@health_bp.get("/ready")
def ready():
    try:
        get_db().execute("SELECT 1").fetchone()
        database = "ok"
    except Exception:
        database = "error"
    status_code = 200 if database == "ok" else 503
    return jsonify({"status": "ready", "database": database}), status_code
