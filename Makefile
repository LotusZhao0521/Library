.PHONY: install dev dev-backend dev-frontend format lint ci build clean docker-up docker-down docker-build help

# ============================================================
#  图书管理系统 Makefile
# ============================================================

# 从根目录 .env 读取配置
-include .env
export
BACKEND_HOST ?= 0.0.0.0
BACKEND_PORT ?= 8000
FRONTEND_PORT ?= 5173

help: ## 显示帮助信息
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

# ------------------------------------------------------------
#  安装
# ------------------------------------------------------------

install: ## 安装所有依赖
	@echo "📦 安装后端依赖..."
	cd backend && uv sync
	@echo "📦 安装前端依赖..."
	cd frontend && npm install
	@echo "✅ 安装完成"

# ------------------------------------------------------------
#  开发
# ------------------------------------------------------------

dev: ## 启动前后端开发服务器
	@./start.sh

dev-backend: ## 仅启动后端开发服务器
	cd backend && uv run uvicorn app.main:app --host $(BACKEND_HOST) --port $(BACKEND_PORT) --reload

dev-frontend: ## 仅启动前端开发服务器
	cd frontend && VITE_BACKEND_PORT=$(BACKEND_PORT) npx vite --host 0.0.0.0 --port $(FRONTEND_PORT)

# ------------------------------------------------------------
#  代码质量
# ------------------------------------------------------------

format: ## 格式化代码
	@echo "🎨 格式化后端代码..."
	cd backend && uv run ruff format app/
	cd backend && uv run ruff check --fix app/
	@echo "✅ 格式化完成"

lint: ## 检查代码规范
	@echo "🔍 检查后端代码..."
	cd backend && uv run ruff check app/
	@echo "🔍 检查前端类型..."
	cd frontend && npx vue-tsc --noEmit
	@echo "✅ 检查通过"

ci: lint ## CI 流水线：lint + type check
	@echo "✅ CI 检查全部通过"

# ------------------------------------------------------------
#  构建
# ------------------------------------------------------------

build: ## 构建前端生产版本
	cd frontend && npm run build

# ------------------------------------------------------------
#  Docker
# ------------------------------------------------------------

docker-build: ## 构建 Docker 镜像
	docker compose build

docker-up: ## 启动 Docker 容器
	docker compose up -d
	@echo ""
	@echo "🚀 服务已启动:"
	@echo "   http://localhost (前端 + API)"
	@echo ""

docker-down: ## 停止 Docker 容器
	docker compose down

docker-logs: ## 查看 Docker 日志
	docker compose logs -f

# ------------------------------------------------------------
#  清理
# ------------------------------------------------------------

clean: ## 清理构建产物和缓存
	rm -rf frontend/dist
	rm -rf backend/__pycache__ backend/**/__pycache__
	rm -rf backend/.ruff_cache
	find backend -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "🧹 清理完成"
