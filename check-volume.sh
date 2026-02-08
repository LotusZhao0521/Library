#!/bin/bash

# Docker 卷查看工具

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}    Docker 卷查看工具${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 1. 列出所有卷
echo -e "${YELLOW}[1] 列出所有 Docker 卷：${NC}"
docker volume ls
echo ""

# 2. 查找当前项目的卷
echo -e "${YELLOW}[2] 查找 library 项目的卷：${NC}"
docker volume ls | grep library || echo "未找到 library 相关的卷"
echo ""

# 3. 查看卷的详细信息
VOLUME_NAME=$(docker volume ls --format "{{.Name}}" | grep -E "library.*db.*data" | head -1)

if [ -z "$VOLUME_NAME" ]; then
    echo -e "${YELLOW}[3] 未找到 library-db-data 卷${NC}"
    echo ""
    echo "提示：卷名可能是以下之一："
    echo "  - library_library-db-data"
    echo "  - library-db-data"
    echo ""
    echo "请手动指定卷名查看："
    echo "  docker volume inspect <卷名>"
else
    echo -e "${YELLOW}[3] 查看卷详细信息：${NC}"
    echo -e "${BLUE}卷名: $VOLUME_NAME${NC}"
    docker volume inspect "$VOLUME_NAME"
    echo ""
    
    # 4. 查看卷的挂载点
    echo -e "${YELLOW}[4] 卷的挂载点（Linux）：${NC}"
    MOUNTPOINT=$(docker volume inspect "$VOLUME_NAME" --format '{{ .Mountpoint }}')
    echo "$MOUNTPOINT"
    echo ""
    
    # 5. 查看卷中的文件
    echo -e "${YELLOW}[5] 查看卷中的文件：${NC}"
    if [ -d "$MOUNTPOINT" ]; then
        echo "使用 sudo 查看卷内容："
        echo "  sudo ls -lah $MOUNTPOINT"
        echo ""
        sudo ls -lah "$MOUNTPOINT" 2>/dev/null || echo "需要 sudo 权限查看"
    else
        echo "无法直接访问挂载点（可能在不同系统上）"
    fi
    echo ""
    
    # 6. 通过容器查看数据库文件
    echo -e "${YELLOW}[6] 通过容器查看数据库文件：${NC}"
    if docker ps --format "{{.Names}}" | grep -q "library-backend"; then
        echo "检查容器内的数据库文件："
        docker exec library-backend ls -lh /app/data/ 2>/dev/null || echo "容器未运行或路径不存在"
        echo ""
        echo "查看数据库文件大小："
        docker exec library-backend sh -c "test -f /app/data/library.db && du -h /app/data/library.db || echo '数据库文件不存在'" 2>/dev/null || echo "无法访问容器"
    else
        echo "library-backend 容器未运行"
    fi
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}    常用命令${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "1. 列出所有卷："
echo -e "   ${BLUE}docker volume ls${NC}"
echo ""
echo "2. 查看卷详细信息："
echo -e "   ${BLUE}docker volume inspect <卷名>${NC}"
echo ""
echo "3. 查看卷的挂载点："
echo -e "   ${BLUE}docker volume inspect <卷名> --format '{{ .Mountpoint }}'${NC}"
echo ""
echo "4. 通过容器查看数据库："
echo -e "   ${BLUE}docker exec library-backend ls -lh /app/data/${NC}"
echo ""
echo "5. 从容器复制数据库文件："
echo -e "   ${BLUE}docker cp library-backend:/app/data/library.db ./backup.db${NC}"
echo ""
echo "6. 删除卷（⚠️ 会删除所有数据）："
echo -e "   ${BLUE}docker volume rm <卷名>${NC}"
echo ""
