"""控制器层公共工具：仅做请求解析，不含业务逻辑。"""

from __future__ import annotations

from flask import request

from ..errors import BadRequest


def get_json_body() -> dict:
    """解析 JSON 对象请求体；无请求体时视为 {}；非法 JSON 抛 BadRequest。"""
    if not request.get_data(cache=True):
        return {}
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise BadRequest("请求体必须是合法的 JSON 对象")
    return data
