"""手写 CORS：显式来源白名单，不使用通配符，不引入额外依赖。"""

from __future__ import annotations

from flask import Flask, request

from ..config import ALLOWED_ORIGINS


def setup_cors(app: Flask) -> None:
    @app.before_request
    def _handle_preflight():
        # 预检请求直接短路，由 after_request 统一补 CORS 响应头
        if request.method == "OPTIONS":
            return app.response_class(status=204)
        return None

    @app.after_request
    def _apply_cors_headers(response):
        origin = request.headers.get("Origin")
        response.headers.add("Vary", "Origin")
        if origin in ALLOWED_ORIGINS:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            response.headers["Access-Control-Max-Age"] = "86400"
        return response
