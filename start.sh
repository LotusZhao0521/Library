#!/bin/bash

# 图书管理系统 - 一键启动脚本
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"
ENV_FILE="$PROJECT_DIR/.env"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 从 .env 读取配置
if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | grep -v '^\s*$' | xargs)
fi

BACKEND_HOST="${BACKEND_HOST:-0.0.0.0}"
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}    图书管理系统 - 启动中...${NC}"
echo -e "${GREEN}========================================${NC}"

# 检查 uv
if ! command -v uv &> /dev/null; then
    echo -e "${RED}错误: 未找到 uv，请先安装: curl -LsSf https://astral.sh/uv/install.sh | sh${NC}"
    exit 1
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}错误: 未找到 node，请先安装 Node.js 18+${NC}"
    exit 1
fi

# 安装后端依赖
echo -e "\n${YELLOW}[1/4] 安装后端依赖...${NC}"
cd "$BACKEND_DIR"
uv sync

# 安装前端依赖
echo -e "${YELLOW}[2/4] 安装前端依赖...${NC}"
cd "$FRONTEND_DIR"
npm install --silent

# 启动后端
echo -e "${YELLOW}[3/4] 启动后端服务 (${BACKEND_HOST}:${BACKEND_PORT})...${NC}"
cd "$BACKEND_DIR"
uv run uvicorn app.main:app --host "$BACKEND_HOST" --port "$BACKEND_PORT" --reload &
BACKEND_PID=$!

# 启动前端
echo -e "${YELLOW}[4/4] 启动前端服务 (端口 ${FRONTEND_PORT})...${NC}"
cd "$FRONTEND_DIR"
VITE_BACKEND_PORT="$BACKEND_PORT" npx vite --host 0.0.0.0 --port "$FRONTEND_PORT" &
FRONTEND_PID=$!

# 清理函数
cleanup() {
    echo -e "\n${YELLOW}正在停止服务...${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo -e "${GREEN}服务已停止${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}    启动成功！${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "  前端地址: ${GREEN}http://localhost:${FRONTEND_PORT}${NC}"
echo -e "  后端地址: ${GREEN}http://localhost:${BACKEND_PORT}${NC}"
echo -e "  API 文档: ${GREEN}http://localhost:${BACKEND_PORT}/docs${NC}"
echo -e ""
echo -e "  默认管理员账号: 见 backend/.env"
echo -e "  按 Ctrl+C 停止所有服务"
echo -e "${GREEN}========================================${NC}"

# 等待子进程
wait
