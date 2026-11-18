# Python 学习网站（python-learning-web）

一个从零构建的 Python 交互式学习网站：**基础语法教程 + 练习题 + 学习进度记录**。后端本身就是 Python，边用边学。

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | 原生 HTML / CSS / JavaScript（无构建步骤） |
| 后端 | Flask 3.x（controllers → services → repositories 三层架构） |
| 数据库 | SQLite |
| API | REST / JSON |

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 初始化数据库（建表 + 灌入教程和练习题）
python backend/migrations/migrate.py
python backend/seeds/seed.py

# 3. 启动服务
python backend/run.py
```

浏览器打开 http://localhost:5000

## 功能

- **教程**：6 篇零基础语法教程（简介 / 变量 / 运算符 / 条件 / 循环 / 函数），支持 Markdown 正文与代码示例
- **练习题**：12 道题，代码输入框提交、即时判分（规范化答案比对，不执行任意代码，安全）
- **进度**：自动记录已学完教程与已答对练习，百分比进度条
- **健康检查**：`/api/health`、`/api/ready`

## 目录结构

```
python-learning-web/
├── CONTRACT.md          # API 契约（v1）—— 前后端数据库唯一约定
├── requirements.txt
├── .env.example
├── backend/
│   ├── app/             # 控制器 / 服务 / 仓储 / 中间件
│   ├── migrations/      # 可回滚迁移脚本
│   ├── seeds/           # 种子数据（教程 + 练习题）
│   ├── data/            # SQLite 数据库文件（不提交）
│   └── run.py           # 启动入口
└── frontend/
    ├── index.html
    ├── css/style.css
    └── js/
        ├── api.js       # 类型化 fetch 封装 + 错误映射 + 重试
        └── app.js       # SPA 路由与渲染
```

## API 端点

完整字段定义见 [CONTRACT.md](CONTRACT.md)。

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/health` | 健康检查 |
| GET | `/api/ready` | 就绪检查（含数据库连通性） |
| GET | `/api/lessons` | 教程列表 |
| GET | `/api/lessons/<id>` | 教程详情 |
| GET | `/api/exercises` | 练习题列表 |
| GET | `/api/exercises/<id>` | 题目详情 |
| POST | `/api/exercises/<id>/submit` | 提交代码答案 |
| GET | `/api/progress` | 学习进度汇总 |
| POST | `/api/progress/lessons/<id>` | 标记教程完成 |
| POST | `/api/progress/exercises/<id>` | 标记练习完成 |

## 版本提交

每次功能更新提交到 GitHub：

```bash
git add .
git commit -m "feat: 简短说明"
git push origin HEAD:main
```
