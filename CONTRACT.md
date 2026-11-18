# API 契约（v1）—— 三个模块并行开发的唯一约定

所有模块必须严格遵守本文件。任何字段增删改都必须先改这里，再同步代码。

## 技术栈

- 后端：Flask 3.x + Python 3.10+，分层架构（controllers → services → repositories）
- 数据库：SQLite，文件 `backend/data/learning.db`，通过 `DATABASE_PATH` 环境变量配置
- 前端：原生 HTML/CSS/JS，无构建步骤，通过 `fetch` 调 REST API
- API 前缀：`/api`，所有响应 JSON（除静态页面与健康检查文本）

## 统一响应格式

成功：直接返回资源 JSON（对象或数组），HTTP 200/201。
失败：`{ "error": { "code": "STRING_CODE", "message": "人类可读文案" } }`，HTTP 4xx/5xx。

错误 code 枚举（前后端共享）：
`BAD_REQUEST` `NOT_FOUND` `VALIDATION_ERROR` `INTERNAL_ERROR`

## 端点清单

### 健康检查
- `GET /api/health` → `{ "status": "ok", "service": "python-learning-web" }`（200）
- `GET /api/ready` → `{ "status": "ready", "database": "ok" | "error" }`（200/503）

### 教程 Lessons
- `GET /api/lessons` → 教程摘要数组，按 `order_index` 升序
  ```
  [{ "id": 1, "slug": "variables", "title": "变量与数据类型", "summary": "...", "order_index": 1, "duration_min": 8 }]
  ```
- `GET /api/lessons/<id>` → 教程详情
  ```
  { "id": 1, "slug": "variables", "title": "...", "summary": "...",
    "content_md": "# 标题\n正文（Markdown）...",
    "code_example": "x = 5\nprint(x)",
    "order_index": 1, "duration_min": 8,
    "exercise_ids": [1, 2] }
  ```

### 练习题 Exercises
- `GET /api/exercises` → 练习题摘要数组，按 `order_index` 升序
  ```
  [{ "id": 1, "lesson_id": 1, "title": "打印Hello", "difficulty": "easy", "order_index": 1 }]
  ```
- `GET /api/exercises/<id>` → 题目详情
  ```
  { "id": 1, "lesson_id": 1, "title": "...", "description": "...",
    "starter_code": "# 在此写代码\n",
    "difficulty": "easy", "order_index": 1 }
  ```
- `POST /api/exercises/<id>/submit` → 提交代码（**不真实执行代码**，仅做答案校验，安全优先）
  - 请求体：`{ "code": "print('Hello')" }`
  - 成功响应：`{ "correct": true, "message": "答对了！", "expected": "print('Hello')" }`
  - 失败响应：`{ "correct": false, "message": "再想想，参考提示：...", "expected": null }`
  - 校验规则：去除首尾空白后，与 `expected_answer` 做规范化比较（忽略引号单双差异、忽略空白差异）

### 学习进度 Progress（单用户演示，无需认证）
- `GET /api/progress` → 汇总
  ```
  { "completed_lesson_ids": [1,2], "completed_exercise_ids": [1],
    "total_lessons": 6, "total_exercises": 12, "completion_percent": 17 }
  ```
  - `completion_percent` 公式：`round((已完成教程数 + 已完成练习数) / (教程总数 + 练习总数) * 100)`，夹取到 0-100。上例 (2+1)/(6+12)=16.7 → 17。
- `POST /api/progress/lessons/<id>` → 标记教程完成，请求体 `{}`，响应 `{ "id": 1, "completed": true }`
- `POST /api/progress/exercises/<id>` → 标记练习完成，请求体 `{ "correct": true }`，响应 `{ "id": 1, "completed": true }`

## 数据库表结构

```sql
lessons(id INTEGER PRIMARY KEY AUTOINCREMENT, slug TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL, summary TEXT, content_md TEXT, code_example TEXT,
        order_index INTEGER NOT NULL, duration_min INTEGER DEFAULT 5)

exercises(id INTEGER PRIMARY KEY AUTOINCREMENT, lesson_id INTEGER NOT NULL,
          title TEXT NOT NULL, description TEXT, starter_code TEXT,
          expected_answer TEXT NOT NULL, difficulty TEXT DEFAULT 'easy',
          order_index INTEGER NOT NULL,
          FOREIGN KEY(lesson_id) REFERENCES lessons(id))

progress(id INTEGER PRIMARY KEY AUTOINCREMENT,
         lesson_id INTEGER, exercise_id INTEGER, completed_at TEXT NOT NULL,
         UNIQUE(lesson_id, exercise_id))
```
简化：完成记录用一行，lesson_id 或 exercise_id 其中一个非空。

## 目录边界（Agent 只写自己的目录）

- 后端 Agent：`backend/` 下除 `migrations/` 和 `seeds/` 外的所有文件
- 数据库 Agent：`backend/migrations/`、`backend/seeds/`、`backend/data/`（运行时生成）
- 前端 Agent：`frontend/` 下所有文件
- 根目录公共文件（README.md、.env.example、requirements.txt、.gitignore）：由主 Agent 统一创建，各 Agent 不得修改

## 配置

- `DATABASE_PATH`：默认 `backend/data/learning.db`（相对项目根，通过 `Path` 拼接）
- `FLASK_ENV` / `PORT`：默认 development / 5000
- CORS：开发允许 `http://localhost:5000` 与 `http://127.0.0.1:5000`，显式来源，不用通配符
