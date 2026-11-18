"""类型化错误定义与统一错误处理。

错误 code 严格使用 CONTRACT.md 规定的枚举：
BAD_REQUEST / NOT_FOUND / VALIDATION_ERROR / INTERNAL_ERROR
所有错误响应统一为 {"error": {"code": "...", "message": "..."}}，绝不泄露堆栈。
"""

from __future__ import annotations

from typing import Any

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

CODE_BAD_REQUEST = "BAD_REQUEST"
CODE_NOT_FOUND = "NOT_FOUND"
CODE_VALIDATION_ERROR = "VALIDATION_ERROR"
CODE_INTERNAL_ERROR = "INTERNAL_ERROR"


class AppError(Exception):
    """所有业务异常的基类。"""

    code = CODE_INTERNAL_ERROR
    status_code = 500
    default_message = "服务器内部错误"

    def __init__(
        self,
        message: str | None = None,
        *,
        status_code: int | None = None,
        code: str | None = None,
    ) -> None:
        super().__init__(message or self.default_message)
        self.message = message or self.default_message
        if status_code is not None:
            self.status_code = status_code
        if code is not None:
            self.code = code

    def to_dict(self) -> dict[str, Any]:
        return {"error": {"code": self.code, "message": self.message}}


class BadRequest(AppError):
    code = CODE_BAD_REQUEST
    status_code = 400
    default_message = "请求无效"


class ValidationError(AppError):
    code = CODE_VALIDATION_ERROR
    status_code = 400
    default_message = "参数校验失败"


class NotFoundError(AppError):
    code = CODE_NOT_FOUND
    status_code = 404
    default_message = "资源不存在"


class InternalError(AppError):
    code = CODE_INTERNAL_ERROR
    status_code = 500
    default_message = "服务器内部错误"


def _http_status_to_code(status: int) -> str:
    if status == 404:
        return CODE_NOT_FOUND
    if status == 400 or status == 405 or 400 <= status < 500:
        return CODE_BAD_REQUEST
    return CODE_INTERNAL_ERROR


def register_error_handlers(app: Flask) -> None:
    """注册全局错误处理器。顺序由异常类型 specificity 决定，与注册顺序无关。"""

    @app.errorhandler(AppError)
    def _handle_app_error(error: AppError):
        app.logger.warning(
            "业务异常 code=%s status=%s path=%s message=%s",
            error.code,
            error.status_code,
            request.path,
            error.message,
        )
        return jsonify(error.to_dict()), error.status_code

    @app.errorhandler(HTTPException)
    def _handle_http_exception(error: HTTPException):
        code = _http_status_to_code(error.code or 500)
        message = {
            CODE_NOT_FOUND: "请求的资源不存在",
            CODE_BAD_REQUEST: "请求无效或不被允许",
            CODE_INTERNAL_ERROR: "服务器内部错误",
        }[code]
        return jsonify({"error": {"code": code, "message": message}}), (
            error.code or 500
        )

    @app.errorhandler(Exception)
    def _handle_unexpected_error(error: Exception):
        # 仅服务端记录堆栈；响应绝不携带任何内部信息。
        app.logger.exception("未处理异常 path=%s", request.path)
        return (
            jsonify(
                {
                    "error": {
                        "code": CODE_INTERNAL_ERROR,
                        "message": "服务器内部错误",
                    }
                }
            ),
            500,
        )
