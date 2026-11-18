"""数据库迁移执行器。

用法（在项目根目录执行）：
    python backend/migrations/migrate.py

行为：
    - 读取环境变量 DATABASE_PATH，默认 backend/data/learning.db（相对项目根）。
    - 自动创建数据库文件所在目录。
    - 按文件名顺序执行本目录下的 *.sql 迁移脚本（executescript）。
    - 使用 schema_migrations 表记录已执行版本，保证重复运行幂等。
"""

import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

# migrations -> backend -> 项目根
PROJECT_ROOT = Path(__file__).resolve().parents[2]
MIGRATIONS_DIR = Path(__file__).resolve().parent


def get_database_path() -> Path:
    """解析数据库路径：环境变量优先，相对路径按项目根拼接。"""
    raw = os.environ.get("DATABASE_PATH", "backend/data/learning.db")
    path = Path(raw)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


def ensure_schema_migrations(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version    TEXT PRIMARY KEY,
            applied_at TEXT NOT NULL
        )
        """
    )
    conn.commit()


def applied_versions(conn: sqlite3.Connection) -> set[str]:
    return {row[0] for row in conn.execute("SELECT version FROM schema_migrations")}


def run_migrations(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    try:
        ensure_schema_migrations(conn)

        migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))
        if not migration_files:
            print("未找到任何 .sql 迁移文件，无需执行。")
            return

        done = applied_versions(conn)
        for migration in migration_files:
            version = migration.stem
            if version in done:
                print(f"[跳过] 迁移 {version} 已执行")
                continue

            print(f"[执行] 迁移 {version} <- {migration.name}")
            sql = migration.read_text(encoding="utf-8")
            conn.executescript(sql)
            conn.execute(
                "INSERT INTO schema_migrations (version, applied_at) VALUES (?, ?)",
                (version, datetime.now(timezone.utc).isoformat()),
            )
            conn.commit()
            print(f"[完成] 迁移 {version}")
    finally:
        conn.close()


def main() -> int:
    db_path = get_database_path()
    print(f"数据库路径：{db_path}")
    try:
        run_migrations(db_path)
    except Exception as exc:  # noqa: BLE001 - 迁移属于启动阶段，失败需明确暴露
        print(f"迁移失败：{exc}", file=sys.stderr)
        return 1
    print("数据库初始化完成。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
