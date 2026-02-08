# 公网部署指南

## 通过公网 IP + 端口访问服务

### 1. 修改端口配置

**只需要修改根目录的 `.env` 文件**，设置前端访问端口：

```bash
# 例如：设置为 18081 端口
FRONTEND_HOST_PORT=18081
FRONTEND_PORT=80
FRONTEND_DOMAIN=_
```

**说明：**
- `FRONTEND_HOST_PORT`: 外部访问端口（公网访问时使用的端口）
- `FRONTEND_PORT`: 容器内 nginx 监听端口（通常保持 80）
- `FRONTEND_DOMAIN`: 保持为 `_` 表示接受所有域名/IP 的请求

**重要：**
- ✅ **只需要修改根目录 `.env` 文件**
- ❌ **不需要修改 `backend/.env` 文件**
- 后端端口（默认 8000）不需要暴露到公网，前端通过 nginx 代理访问后端
- 如果未来需要修改后端端口，才需要修改 `backend/.env` 中的 `PORT`，并运行 `./sync-env.sh` 同步

### 2. 重启服务

```bash
# 停止现有服务
docker-compose down

# 重新构建并启动（前端需要重建以应用新配置）
docker-compose up -d --build

# 或者只重建前端
docker-compose up -d --build frontend
```

### 3. 配置防火墙（重要！）

在服务器上开放端口，例如使用 `ufw`：

```bash
# Ubuntu/Debian
sudo ufw allow 18081/tcp
sudo ufw reload

# 或者使用 iptables
sudo iptables -A INPUT -p tcp --dport 18081 -j ACCEPT
```

### 4. 访问服务

配置完成后，通过以下方式访问：

```
http://你的公网IP:18081
```

例如：`http://123.45.67.89:18081`

### 5. 验证配置

检查端口是否正常监听：

```bash
# 检查容器端口映射
docker-compose ps

# 检查端口是否开放
sudo netstat -tlnp | grep 18081
# 或
sudo ss -tlnp | grep 18081
```

### 注意事项

1. **安全建议**：
   - ⚠️ **避免使用标准端口**：不要使用 80（HTTP）或 443（HTTPS）端口，这些端口容易被自动扫描和攻击
   - ✅ **使用非标准端口**：建议使用 18081、8080、3000、8888 等非标准端口
   - 🔒 **生产环境必须使用 HTTPS**：配置 SSL 证书，使用 443 端口（通过反向代理）
   - 🛡️ **考虑使用反向代理**：使用 Nginx、Caddy 等反向代理处理 SSL 和路由
   - 🔑 **定期更新密码和密钥**：修改默认的管理员密码和 SECRET_KEY
   - 🚫 **限制访问来源**：如果可能，配置防火墙规则限制访问 IP

2. **CORS 配置**：
   - 当前后端 CORS 已配置为允许所有来源（`allow_origins=["*"]`）
   - 如果需要限制，可以修改 `backend/app/main.py` 中的 CORS 配置

3. **后端端口**：
   - 后端端口（默认 8000）不需要直接暴露到公网
   - 前端通过 nginx 代理访问后端，后端只在 Docker 网络内通信

4. **域名访问**（可选）：
   - 如果有域名，可以设置 `FRONTEND_DOMAIN=yourdomain.com`
   - 配置 DNS 解析指向你的公网 IP
   - 建议使用反向代理配置 HTTPS

### 常见问题

**Q: 只需要修改根目录的 .env 吗？backend/.env 需要修改吗？**
- ✅ **只需要修改根目录的 `.env` 文件**中的 `FRONTEND_HOST_PORT` 即可
- ❌ **不需要修改 `backend/.env` 文件**
- 原因：前端端口配置与后端无关，后端通过 Docker 内部网络通信，不直接暴露到公网
- 只有在需要修改后端端口时，才需要修改 `backend/.env` 中的 `PORT`，并运行 `./sync-env.sh` 同步

**Q: 无法访问？**
- 检查防火墙是否开放端口
- 检查 docker-compose 服务是否正常运行：`docker-compose ps`
- 检查端口映射是否正确：`docker-compose port frontend 80`

**Q: 如何查看日志？**
```bash
# 查看所有服务日志
docker-compose logs

# 查看前端日志
docker-compose logs frontend

# 实时查看日志
docker-compose logs -f frontend
```

**Q: 如何配置 HTTPS？**
- 推荐使用反向代理（如 Nginx、Caddy）处理 SSL
- 或使用 Let's Encrypt 自动证书
- 修改 nginx 配置添加 SSL 支持
