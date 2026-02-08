#!/bin/bash

# 502 错误修复脚本
# 用于诊断和修复后端连接问题

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}    502 错误诊断和修复工具${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 1. 检查容器状态
echo -e "${YELLOW}[1/6] 检查容器状态...${NC}"
docker-compose ps
echo ""

# 2. 检查后端容器日志
echo -e "${YELLOW}[2/6] 检查后端容器日志（最后30行）...${NC}"
docker-compose logs --tail=30 backend
echo ""

# 3. 检查前端容器日志
echo -e "${YELLOW}[3/6] 检查前端容器日志（最后30行）...${NC}"
docker-compose logs --tail=30 frontend
echo ""

# 4. 检查环境变量
echo -e "${YELLOW}[4/6] 检查环境变量配置...${NC}"
echo "根目录 .env 文件："
if [ -f .env ]; then
    grep -E "^(PORT|FRONTEND_PORT|FRONTEND_HOST_PORT)=" .env || echo "未找到相关配置"
else
    echo -e "${RED}错误: .env 文件不存在${NC}"
fi
echo ""
echo "backend/.env 文件："
if [ -f backend/.env ]; then
    grep -E "^(PORT|DATABASE_URL)=" backend/.env || echo "未找到相关配置"
else
    echo -e "${RED}错误: backend/.env 文件不存在${NC}"
fi
echo ""

# 5. 检查容器内的环境变量
echo -e "${YELLOW}[5/6] 检查容器内的环境变量...${NC}"
echo "前端容器 BACKEND_PORT:"
docker exec library-frontend env | grep BACKEND_PORT || echo -e "${RED}未找到 BACKEND_PORT${NC}"
echo "后端容器 PORT:"
docker exec library-backend env | grep PORT || echo -e "${RED}未找到 PORT${NC}"
echo ""

# 6. 测试容器间连接
echo -e "${YELLOW}[6/6] 测试容器间连接...${NC}"
echo "从前端容器测试后端连接："
docker exec library-frontend wget -q -O- --timeout=3 http://backend:8000/docs 2>&1 | head -3 || echo -e "${RED}无法连接到后端服务${NC}"
echo ""

# 修复建议
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}    修复建议${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "如果后端容器未运行或启动失败，请执行："
echo -e "${YELLOW}docker-compose restart backend${NC}"
echo ""
echo "如果问题仍然存在，请尝试完全重建："
echo -e "${YELLOW}docker-compose down${NC}"
echo -e "${YELLOW}docker-compose up -d --build${NC}"
echo ""
echo "查看实时日志："
echo -e "${YELLOW}docker-compose logs -f backend${NC}"
echo ""
