"""中间件注册入口。

注意：Flask 的 after_request 按注册逆序执行，因此这里先注册日志、后注册 CORS，
可保证 CORS 头最终仍被附加在响应上（两个处理器互不依赖对方结果）。
"""

from __future__ import annotations

from flask import Flask

from .cors import setup_cors
from .logging import setup_logging


def register_middleware(app: Flask) -> None:
    setup_logging(app)
    setup_cors(app)
