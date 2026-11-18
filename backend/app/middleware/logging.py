"""请求上下文与结构化访问日志中间件。"""

from __future__ import annotations

import json
import logging
import time
import uuid
from typing import Any

from flask import Flask, g, request

REQUEST_ID_HEADER = "X-Request-ID"

_access_logger = logging.getLogger("app.access")
_access_logger.setLevel(logging.INFO)
_access_logger.propagate = False


class _JsonFormatter(logging.Formatter):
    """把 dict 消息序列化为单行 JSON；绝不使用 getMessage() 拼装堆栈。"""

    def format(self, record: logging.LogRecord) -> str:
        payload: Any = record.msg
        if not isinstance(payload, dict):
            payload = {"message": record.getMessage()}
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


if not _access_logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(_JsonFormatter())
    _access_logger.addHandler(_handler)


def setup_logging(app: Flask) -> None:
    @app.before_request
    def _assign_request_context() -> None:
        g.request_id = uuid.uuid4().hex[:8]
        g._request_started_at = time.perf_counter()

    @app.after_request
    def _emit_access_log(response):
        request_id = getattr(g, "request_id", "-")
        started_at = getattr(g, "_request_started_at", None)
        duration_ms = (
            round((time.perf_counter() - started_at) * 1000, 2)
            if started_at is not None
            else 0.0
        )
        response.headers[REQUEST_ID_HEADER] = request_id
        # 仅记录非敏感元数据：请求体、查询参数、Cookie、Header 一律不记录
        _access_logger.info(
            {
                "method": request.method,
                "path": request.path,
                "status": response.status_code,
                "duration_ms": duration_ms,
                "request_id": request_id,
            }
        )
        return response
