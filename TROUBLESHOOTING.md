# 无法访问 127.0.0.1:18081 故障排除指南

## 已修复的问题

✅ **nginx配置格式问题**：已将 `${VARIABLE:-default}` 格式改为 `$VARIABLE` 格式，兼容nginx:alpine的envsubst模板系统。

## 排查步骤

### 1. 确认服务已启动

```bash
# 检查容器状态
docker-compose ps

# 应该看到两个容器都在运行：
# - library-backend (状态: Up)
# - library-frontend (状态: Up)
```

### 2. 检查端口映射

```bash
# 检查前端端口映射
docker-compose port frontend 80

# 应该输出类似：0.0.0.0:18081
```

### 3. 检查环境变量

```bash
# 确认 .env 文件中的配置
cat .env | grep FRONTEND_HOST_PORT

# 应该显示：FRONTEND_HOST_PORT=18081
```

### 4. 查看容器日志

```bash
# 查看前端容器日志
docker-compose logs frontend

# 查看后端容器日志
docker-compose logs backend

# 实时查看日志
docker-compose logs -f frontend
```

### 5. 检查nginx配置是否正确生成

```bash
# 进入前端容器
docker exec -it library-frontend sh

# 查看生成的nginx配置
cat /etc/nginx/conf.d/default.conf

# 应该看到：
# listen 80;
# proxy_pass http://backend:8000;
```

### 6. 测试容器内部连接

```bash
# 测试前端容器内的nginx
docker exec library-frontend wget -O- http://localhost:80

# 测试后端容器
docker exec library-backend wget -O- http://localhost:8000/api/v1/health 2>/dev/null || echo "后端可能没有健康检查端点"
```

## 常见问题及解决方案

### 问题1: 容器未启动

**症状**: `docker-compose ps` 显示容器状态为 `Exit` 或 `Restarting`

**解决方案**:
```bash
# 停止所有容器
docker-compose down

# 重新构建并启动
docker-compose up -d --build

# 查看日志找出错误
docker-compose logs
```

### 问题2: 端口被占用

**症状**: 启动时出现 `port is already allocated` 错误

**解决方案**:
```bash
# 检查端口占用
sudo lsof -i :18081
# 或
sudo netstat -tlnp | grep 18081

# 停止占用端口的进程，或修改 .env 中的 FRONTEND_HOST_PORT
```

### 问题3: nginx配置未正确替换

**症状**: 日志显示 `nginx: [emerg] invalid number in "listen" directive`

**解决方案**:
```bash
# 确保环境变量已传递
docker exec library-frontend env | grep FRONTEND_PORT
docker exec library-frontend env | grep BACKEND_PORT

# 如果环境变量不存在，需要重启容器
docker-compose restart frontend
```

### 问题4: 后端连接失败

**症状**: 前端可以访问，但API请求失败

**解决方案**:
```bash
# 检查后端是否正常运行
docker-compose logs backend

# 测试后端连接
curl http://127.0.0.1:8000/api/v1/health

# 检查docker网络
docker network inspect library_default
```

### 问题5: 防火墙阻止访问

**症状**: 容器运行正常，但无法从外部访问

**解决方案**:
```bash
# WSL2/Linux: 检查防火墙
sudo ufw status
sudo iptables -L -n | grep 18081

# 如果需要，开放端口
sudo ufw allow 18081/tcp
```

## 快速修复命令

如果以上步骤都无法解决问题，尝试完全重建：

```bash
# 1. 停止并删除所有容器和卷
docker-compose down -v

# 2. 清理构建缓存（可选）
docker-compose build --no-cache

# 3. 重新启动
docker-compose up -d

# 4. 查看日志
docker-compose logs -f
```

## 验证访问

修复后，应该能够通过以下方式访问：

```bash
# 浏览器访问
http://127.0.0.1:18081
http://localhost:18081

# 命令行测试
curl http://127.0.0.1:18081
```

## 使用诊断脚本

运行我创建的诊断脚本：

```bash
./check-access.sh
```

这个脚本会自动检查以上所有项目并输出诊断信息。
