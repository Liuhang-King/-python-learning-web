-- 迁移 001：初始化数据库表结构
--
-- 回滚顺序（子表优先，避免出现外键依赖）：
--   DROP INDEX IF EXISTS idx_progress_exercise_id;
--   DROP INDEX IF EXISTS idx_progress_lesson_id;
--   DROP INDEX IF EXISTS idx_exercises_lesson_id;
--   DROP TABLE IF EXISTS progress;
--   DROP TABLE IF EXISTS exercises;
--   DROP TABLE IF EXISTS lessons;
--
-- 说明：本脚本由 migrate.py 通过 executescript 执行，请勿在末尾手动删除 schema_migrations 表。

-- 教程表
CREATE TABLE IF NOT EXISTS lessons (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    slug         TEXT UNIQUE NOT NULL,
    title        TEXT NOT NULL,
    summary      TEXT,
    content_md   TEXT,
    code_example TEXT,
    order_index  INTEGER NOT NULL,
    duration_min INTEGER DEFAULT 5
);

-- 练习题表
CREATE TABLE IF NOT EXISTS exercises (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson_id       INTEGER NOT NULL,
    title           TEXT NOT NULL,
    description     TEXT,
    starter_code    TEXT,
    expected_answer TEXT NOT NULL,
    difficulty      TEXT DEFAULT 'easy',
    order_index     INTEGER NOT NULL,
    FOREIGN KEY (lesson_id) REFERENCES lessons (id)
);

-- 学习进度表（一行代表一条完成记录，lesson_id / exercise_id 二选一非空）
CREATE TABLE IF NOT EXISTS progress (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson_id    INTEGER,
    exercise_id  INTEGER,
    completed_at TEXT NOT NULL,
    UNIQUE (lesson_id, exercise_id)
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_exercises_lesson_id    ON exercises (lesson_id);
CREATE INDEX IF NOT EXISTS idx_progress_lesson_id     ON progress (lesson_id);
CREATE INDEX IF NOT EXISTS idx_progress_exercise_id   ON progress (exercise_id);
