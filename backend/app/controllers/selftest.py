"""系统自检控制器。"""

from __future__ import annotations

from flask import Blueprint, jsonify

from ..services import selftest_service

selftest_bp = Blueprint("selftest", __name__, url_prefix="/api")


@selftest_bp.get("/selftest")
def selftest():
    """全量自检：教程/练习完整性、判分自测、数据库连通。只读，不改数据。"""
    report = selftest_service.run_selftest()
    return jsonify(report)
