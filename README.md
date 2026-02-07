# 图书管理系统

一个前后端分离的简易图书管理系统，支持用户管理、图书管理、借阅归还及阅读心得记录。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + TypeScript + Vite + Pinia + Vue Router |
| 后端 | FastAPI + SQLAlchemy + SQLite |
| 包管理 | uv (Python) / npm (Node.js) |
| 部署 | Docker Compose + Nginx |

## 项目结构

```
Library/
├── backend/                  # 后端 (FastAPI)
│   ├── app/
│   │   ├── api/              # API 路由层
│   │   │   ├── dependencies.py   # 认证依赖 (JWT 校验、权限检查)
│   │   │   └── v1/endpoints/     # 接口端点
│   │   │       ├── auth.py       #   登录认证
│   │   │       ├── users.py      #   用户管理
│   │   │       ├── books.py      #   图书管理 + 借阅/归还
│   │   │       └── borrow_records.py  # 借阅记录 + 心得
│   │   ├── core/             # 核心配置
│   │   │   ├── config.py         # 环境变量读取 (pydantic-settings)
│   │   │   ├── database.py       # 数据库引擎 + 会话管理
│   │   │   └── security.py       # JWT 签发 + bcrypt 密码哈希
│   │   ├── models/           # SQLAlchemy ORM 模型
│   │   │   ├── user.py           # 用户表
│   │   │   ├── book.py           # 图书表
│   │   │   └── borrow_record.py  # 借阅记录表
│   │   ├── schemas/          # Pydantic 请求/响应模型
│   │   ├── repositories/     # 数据访问层
│   │   ├── services/         # 业务逻辑层
│   │   └── main.py           # 应用入口 + 启动事件
│   ├── .env                  # 后端环境变量 (不提交)
│   ├── .env.example          # 环境变量模板
│   ├── pyproject.toml        # Python 依赖 + 工具配置
│   ├── uv.lock               # 依赖锁定文件
│   └── Dockerfile
├── frontend/                 # 前端 (Vue 3)
│   ├── src/
│   │   ├── api/index.ts      # Axios 请求封装 + 拦截器
│   │   ├── stores/auth.ts    # Pinia 认证状态 (token、用户信息)
│   │   ├── router/index.ts   # 路由定义 + 导航守卫 (权限控制)
│   │   ├── types/index.ts    # TypeScript 类型定义
│   │   ├── components/       # 通用组件 (导航栏)
│   │   ├── views/            # 页面组件
│   │   │   ├── LoginView.vue         # 登录
│   │   │   ├── DashboardView.vue     # 图书列表首页
│   │   │   ├── BookDetailView.vue    # 图书详情 + 借阅/归还
│   │   │   ├── MyBorrowsView.vue     # 我的借阅 + 阅读心得
│   │   │   ├── ChangePasswordView.vue # 修改密码
│   │   │   ├── AdminBooksView.vue    # [管理员] 图书增删改
│   │   │   └── AdminUsersView.vue    # [管理员] 用户创建/角色管理
│   │   ├── App.vue
│   │   ├── main.ts
│   │   └── style.css         # 全局样式 (类苹果简约风格)
│   ├── nginx.conf            # 生产环境 Nginx 配置
│   ├── vite.config.ts
│   └── Dockerfile
├── .env                      # 项目级配置 (端口等，不提交)
├── .env.example              # 项目级配置模板
├── docker-compose.yml
├── Makefile
├── start.sh                  # 一键启动脚本 (开发)
└── README.md
```

## 功能说明

### 用户体系

| 角色 | 权限 |
|------|------|
| 管理员 | 创建用户（设置初始密码）、提升/降级用户角色、增删改图书 |
| 普通用户 | 浏览图书、借阅/归还（同时最多借 1 本）、撰写阅读心得 |

- 初始管理员账号密码在 `backend/.env` 中配置，应用启动时自动创建
- 所有用户均可自行修改密码

### API 接口

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/api/v1/auth/login` | 登录获取 JWT | 公开 |
| GET | `/api/v1/users/me` | 获取当前用户信息 | 已登录 |
| PUT | `/api/v1/users/me/password` | 修改密码 | 已登录 |
| POST | `/api/v1/users/` | 创建用户 | 管理员 |
| GET | `/api/v1/users/` | 用户列表 | 管理员 |
| PUT | `/api/v1/users/{id}/role` | 修改用户角色 | 管理员 |
| GET | `/api/v1/books/` | 图书列表 | 已登录 |
| GET | `/api/v1/books/{id}` | 图书详情 | 已登录 |
| POST | `/api/v1/books/` | 添加图书 | 管理员 |
| PUT | `/api/v1/books/{id}` | 编辑图书 | 管理员 |
| DELETE | `/api/v1/books/{id}` | 删除图书 | 管理员 |
| POST | `/api/v1/books/{id}/borrow` | 借阅 | 已登录 |
| POST | `/api/v1/books/{id}/return` | 归还 | 已登录 |
| GET | `/api/v1/books/{id}/records` | 图书借阅记录 | 已登录 |
| GET | `/api/v1/borrow-records/` | 我的借阅记录 | 已登录 |
| PUT | `/api/v1/borrow-records/{id}/note` | 更新阅读心得 | 已登录 |

交互式 API 文档：启动后端后访问 `http://localhost:8000/docs`

## 环境要求

- **Python** >= 3.12
- **Node.js** >= 18
- **uv** (Python 包管理器)：`curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Docker + Docker Compose** (仅服务器部署需要)

## 本地开发

### 1. 配置环境变量

```bash
# 项目级配置（端口）
cp .env.example .env

# 后端配置（密钥、管理员账号、数据库）
cp backend/.env.example backend/.env
# 按需修改 backend/.env 中的 SECRET_KEY、ADMIN_USERNAME、ADMIN_PASSWORD
```

### 2. 一键启动

```bash
# 方式一：使用启动脚本（自动安装依赖 + 启动前后端）
./start.sh

# 方式二：使用 Makefile
make install   # 安装依赖
make dev       # 启动前后端
```

启动后访问：

| 服务 | 地址 |
|------|------|
| 前端 | http://localhost:5173 |
| 后端 API | http://localhost:8000 |
| API 文档 | http://localhost:8000/docs |

端口可在根目录 `.env` 中修改。

### 3. 单独启动

```bash
# 仅启动后端
make dev-backend

# 仅启动前端
make dev-frontend
```

### 4. 代码质量

```bash
make format    # 格式化代码 (ruff)
make lint      # 代码检查 (ruff + vue-tsc)
make ci        # CI 检查（等同于 lint）
```

## 服务器部署 (Docker)

### 1. 准备配置文件

```bash
# 项目级配置
cp .env.example .env

# 后端配置（务必修改 SECRET_KEY）
cp backend/.env.example backend/.env
```

编辑 `backend/.env`，设置安全的生产配置：

```env
SECRET_KEY=<生成一个随机字符串>
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<设置强密码>
DATABASE_URL=sqlite+aiosqlite:///./data/library.db
```

### 2. 构建并启动

```bash
# 构建镜像
make docker-build

# 启动服务（后台运行）
make docker-up

# 或者直接用 docker compose
docker compose up -d --build
```

启动后访问 `http://<服务器IP>` 即可使用（端口 80）。

### 3. 运维命令

```bash
# 查看日志
make docker-logs

# 停止服务
make docker-down

# 重新构建并启动（代码更新后）
docker compose up -d --build
```

### 部署架构

```
客户端 → :80 Nginx (frontend 容器)
                ├── /           → Vue 静态文件
                └── /api/*      → 反向代理 → backend 容器:8000
```

- **frontend 容器**：Nginx 托管 Vue 构建产物，同时反向代理 API 请求
- **backend 容器**：Uvicorn 运行 FastAPI 应用
- **数据持久化**：SQLite 数据库文件通过 Docker Volume 持久化

## Makefile 命令速查

| 命令 | 说明 |
|------|------|
| `make help` | 显示所有可用命令 |
| `make install` | 安装全部依赖 |
| `make dev` | 启动前后端开发服务器 |
| `make dev-backend` | 仅启动后端 |
| `make dev-frontend` | 仅启动前端 |
| `make format` | 格式化代码 |
| `make lint` | 代码规范检查 |
| `make ci` | CI 流水线 |
| `make build` | 构建前端生产版本 |
| `make docker-build` | 构建 Docker 镜像 |
| `make docker-up` | 启动 Docker 容器 |
| `make docker-down` | 停止 Docker 容器 |
| `make docker-logs` | 查看容器日志 |
| `make clean` | 清理缓存和构建产物 |

## 默认账号

| 字段 | 默认值 | 配置位置 |
|------|--------|----------|
| 用户名 | admin | `backend/.env` → `ADMIN_USERNAME` |
| 密码 | admin123 | `backend/.env` → `ADMIN_PASSWORD` |

首次启动时自动创建，后续重启不会覆盖已修改的密码。
