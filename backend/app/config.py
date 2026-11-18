"""集中配置管理。

所有配置均从环境变量读取，缺失时使用契约约定的默认值，存在但非法时启动即失败。
不包含任何硬编码密钥。
"""

from __future__ import annotations

import os
from pathlib import Path

# 项目根目录：python-learning-web/（本文件位于 backend/app/ 下）
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_DATABASE_PATH = "backend/data/learning.db"
DEFAULT_FLASK_ENV = "development"
DEFAULT_PORT = 5000

VALID_ENVIRONMENTS = frozenset({"development", "production", "testing"})

# CORS 显式白名单，禁止通配符
ALLOWED_ORIGINS = frozenset(
    {
        "http://localhost:5000",
        "http://127.0.0.1:5000",
    }
)


def _read(name: str, default: str) -> str:
    """读取环境变量；空字符串视为未设置。"""
    value = os.environ.get(name)
    return default if value is None or value.strip() == "" else value.strip()


def _validate_port(raw: str) -> int:
    try:
        port = int(raw)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"PORT 必须是整数，当前值：{raw!r}") from exc
    if not 1 <= port <= 65535:
        raise ValueError(f"PORT 必须在 1-65535 之间，当前值：{port}")
    return port


def _validate_env(raw: str) -> str:
    env = raw.lower()
    if env not in VALID_ENVIRONMENTS:
        raise ValueError(
            f"FLASK_ENV 必须是 {sorted(VALID_ENVIRONMENTS)} 之一，当前值：{raw!r}"
        )
    return env


def _resolve_database_path(raw: str) -> Path:
    path = Path(raw).expanduser()
    return path if path.is_absolute() else (PROJECT_ROOT / path).resolve()


# 模块导入时即完成读取与校验：配置非法则进程无法启动。
FLASK_ENV = _validate_env(_read("FLASK_ENV", DEFAULT_FLASK_ENV))
PORT = _validate_port(_read("PORT", str(DEFAULT_PORT)))
DATABASE_PATH = _resolve_database_path(_read("DATABASE_PATH", DEFAULT_DATABASE_PATH))


class Config:
    """供 create_app 使用的配置对象（所有值均来自上方集中计算结果）。"""

    DEBUG = FLASK_ENV == "development"
    TESTING = FLASK_ENV == "testing"
    FLASK_ENV = FLASK_ENV
    PORT = PORT
    DATABASE_PATH = str(DATABASE_PATH)
    ALLOWED_ORIGINS = ALLOWED_ORIGINS
    JSON_SORT_KEYS = False
    # 静态资源目录：frontend/ 与 backend/ 同级
    FRONTEND_DIR = str(PROJECT_ROOT / "frontend")
