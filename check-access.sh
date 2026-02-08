#!/bin/bash

echo "=== 检查服务状态 ==="
echo ""
echo "1. 检查 Docker 容器状态："
docker-compose ps
echo ""

echo "2. 检查端口映射："
docker-compose port frontend 80 2>/dev/null || echo "无法获取端口映射"
echo ""

echo "3. 检查前端容器日志（最后20行）："
docker-compose logs --tail=20 frontend
echo ""

echo "4. 检查后端容器日志（最后20行）："
docker-compose logs --tail=20 backend
echo ""

echo "5. 检查环境变量："
echo "FRONTEND_HOST_PORT: ${FRONTEND_HOST_PORT:-未设置}"
echo "FRONTEND_PORT: ${FRONTEND_PORT:-未设置}"
echo "PORT: ${PORT:-未设置}"
echo ""

echo "6. 测试端口连接："
if command -v curl >/dev/null 2>&1; then
    echo "测试 http://127.0.0.1:${FRONTEND_HOST_PORT:-18081} ..."
    curl -I http://127.0.0.1:${FRONTEND_HOST_PORT:-18081} 2>&1 | head -5
else
    echo "curl 未安装，跳过连接测试"
fi
