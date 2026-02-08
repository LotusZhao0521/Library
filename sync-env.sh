#!/bin/bash
# 同步 backend/.env 中的 PORT 到根目录 .env
# 使用方法: ./sync-env.sh

BACKEND_ENV="./backend/.env"
ROOT_ENV="./.env"

if [ ! -f "$BACKEND_ENV" ]; then
    echo "错误: $BACKEND_ENV 不存在"
    exit 1
fi

# 从 backend/.env 读取 PORT
PORT=$(grep "^PORT=" "$BACKEND_ENV" | cut -d '=' -f2)

if [ -z "$PORT" ]; then
    echo "警告: backend/.env 中没有找到 PORT，使用默认值 8000"
    PORT=8000
fi

# 更新根目录 .env
if [ -f "$ROOT_ENV" ]; then
    # 如果根目录 .env 中已有 PORT，则更新它；否则追加
    if grep -q "^PORT=" "$ROOT_ENV"; then
        sed -i "s/^PORT=.*/PORT=$PORT/" "$ROOT_ENV"
        echo "✓ 已更新根目录 .env 中的 PORT=$PORT"
    else
        echo "PORT=$PORT" >> "$ROOT_ENV"
        echo "✓ 已在根目录 .env 中添加 PORT=$PORT"
    fi
else
    echo "警告: 根目录 .env 不存在，创建新文件"
    echo "PORT=$PORT" > "$ROOT_ENV"
    echo "✓ 已创建根目录 .env，PORT=$PORT"
fi

echo "同步完成！现在两个 .env 文件中的 PORT 已保持一致"
