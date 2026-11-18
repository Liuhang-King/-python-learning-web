"""控制器层注册入口。"""

from __future__ import annotations

from flask import Flask

from .exercises import exercises_bp
from .health import health_bp
from .lessons import lessons_bp
from .progress import progress_bp

_ALL_BLUEPRINTS = (health_bp, lessons_bp, exercises_bp, progress_bp)


def register_controllers(app: Flask) -> None:
    for blueprint in _ALL_BLUEPRINTS:
        app.register_blueprint(blueprint)
