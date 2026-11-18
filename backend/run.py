"""后端启动入口。

用法（在 python-learning-web/ 根目录）：
    python backend/run.py
"""

from __future__ import annotations

import signal
import sys
from pathlib import Path

# 保证从任意工作目录执行时都能导入 backend/app 包
_BACKEND_DIR = str(Path(__file__).resolve().parent)
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)

from app import create_app  # noqa: E402
from app.config import Config  # noqa: E402

app = create_app()

_stopping = False


def _handle_signal(signum, frame) -> None:
    """SIGINT/SIGTERM 时退出主循环，由解释器完成资源回收。"""
    global _stopping
    if not _stopping:
        _stopping = True
        print(f"\n收到信号 {signum}，服务正在退出...", flush=True)
        raise SystemExit(0)


def main() -> None:
    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT, _handle_signal)
    app.run(
        host="0.0.0.0",
        port=Config.PORT,
        debug=Config.DEBUG,
        # 关闭 reloader，避免子进程绕过信号处理、造成退出后端口残留
        use_reloader=False,
    )


if __name__ == "__main__":
    main()
