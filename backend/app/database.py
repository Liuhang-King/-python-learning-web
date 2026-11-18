"""SQLite 数据库访问基础设施。

连接按请求缓存于 flask.g，请求结束（teardown）时统一关闭。
所有查询参数化，杜绝 SQL 注入。
"""

from __future__ import annotations

import sqlite3
from typing import Any, Iterable

from flask import current_app, g

from .errors import InternalError


def get_db() -> sqlite3.Connection:
    """取得当前请求/应用上下文中的数据库连接（惰性创建）。"""
    if "db" not in g:
        connection = sqlite3.connect(
            current_app.config["DATABASE_PATH"],
            timeout=10,
            # 让外键约束生效（契约中 exercises / progress 含外键）
            isolation_level=None,
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        g.db = connection
    return g.db


def close_db(error: BaseException | None = None) -> None:
    """teardown_appcontext 回调，关闭并移除连接。"""
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def is_missing_table(exc: sqlite3.Error) -> bool:
    return isinstance(exc, sqlite3.OperationalError) and "no such table" in str(
        exc
    ).lower()


def execute(
    sql: str, params: Iterable[Any] = ()
) -> sqlite3.Cursor:
    """统一执行入口：把「表不存在」转换为 503 的 INTERNAL_ERROR。"""
    try:
        return get_db().execute(sql, tuple(params))
    except sqlite3.OperationalError as exc:
        if is_missing_table(exc):
            raise InternalError(
                "数据库未初始化，请先执行数据库迁移", status_code=503
            ) from exc
        raise
