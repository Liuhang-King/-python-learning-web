"""Flask 应用工厂。

职责：加载集中配置 → 注册全局错误处理 → 注册中间件 → 注册控制器蓝图
→ 注册数据库连接回收 → 托管前端静态资源。
"""

from __future__ import annotations

from typing import Any, Mapping

from flask import Flask

from .config import Config
from .controllers import register_controllers
from .database import close_db
from .errors import register_error_handlers
from .middleware import register_middleware

__all__ = ["create_app"]


def create_app(config_overrides: Mapping[str, Any] | None = None) -> Flask:
    app = Flask(
        __name__,
        static_folder=Config.FRONTEND_DIR,
        static_url_path="",
    )
    app.config.from_object(Config)
    if config_overrides:
        app.config.update(config_overrides)

    register_error_handlers(app)
    register_middleware(app)
    register_controllers(app)

    app.teardown_appcontext(close_db)

    @app.get("/")
    def index():
        return app.send_static_file("index.html")

    return app
