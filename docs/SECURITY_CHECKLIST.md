# 提交前安全检查清单

本文档说明项目中**不应提交到代码仓库**的内容及当前防护措施。

## 已正确忽略（不会随 git 提交）

| 内容 | 说明 | .gitignore 规则 |
|------|------|------------------|
| 根目录 `.env` | 项目级配置（端口等） | `.env` |
| `backend/.env` | 后端密钥、管理员账号、数据库 URL | `.env`、`backend/.env` |
| `backend/library.db` | SQLite 数据库文件 | `*.db`、`backend/*.db` |
| `backend/.venv/` | Python 虚拟环境 | `.venv/` |
| `frontend/node_modules/` | Node 依赖 | `node_modules/` |
| `frontend/dist/` | 前端构建产物 | `dist/` |
| 各类缓存/日志 | `__pycache__`、`*.log` 等 | 见 .gitignore |

## 可安全提交的内容

| 文件 | 说明 |
|------|------|
| `.env.example`、`backend/.env.example` | 仅含占位符或示例值，无真实密钥 |
| `backend/app/core/config.py` 中的默认值 | 仅在没有 .env 时生效，生产环境必须配置 .env |

## 建议

1. **首次 push 前**执行一次：  
   `git status` 确认列表中没有 `.env`、`backend/.env`、`*.db`。
2. **生产部署**时务必在服务器上单独创建 `backend/.env`，并设置强 `SECRET_KEY` 和 `ADMIN_PASSWORD`，不要使用 .env.example 中的示例值。
