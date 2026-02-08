# 公网访问故障排除指南

## 问题现象
- ✅ 本地访问正常：`curl http://127.0.0.1:18081` 成功
- ❌ 公网访问失败：`curl http://公网IP:18081` 失败

## 已确认正常的部分

✅ **Docker端口映射正确**：
```
0.0.0.0:18081->80/tcp
```
端口已绑定到所有网络接口（0.0.0.0），不是只绑定到127.0.0.1

✅ **端口正在监听**：
```
LISTEN 0      4096                *:18081            *:*
```
端口18081正在监听所有接口

## 需要检查的问题

### 1. 阿里云安全组配置（最常见原因）

**问题**：阿里云ECS实例的安全组默认只开放22（SSH）和3389（RDP）端口，其他端口需要手动添加规则。

**解决步骤**：

1. **登录阿里云控制台**
   - 进入：ECS实例 → 网络与安全 → 安全组

2. **添加入站规则**
   - 点击"配置规则" → "入方向" → "添加安全组规则"
   - 配置如下：
     ```
     规则方向：入方向
     授权策略：允许
     协议类型：自定义TCP
     端口范围：18081/18081
     授权对象：0.0.0.0/0（允许所有IP访问）
      ```
   - 描述：`Library Frontend Port`
   - 点击"保存"

3. **验证规则**
   - 确认规则已添加并生效
   - 等待1-2分钟让规则生效

### 2. 服务器防火墙（ufw/iptables）

#### 检查ufw状态

```bash
# 检查ufw状态
sudo ufw status

# 如果ufw是active状态，需要开放端口
sudo ufw allow 18081/tcp
sudo ufw reload

# 验证
sudo ufw status | grep 18081
```

#### 检查iptables规则

```bash
# 查看iptables规则
sudo iptables -L -n -v | grep 18081

# 如果端口被阻止，添加规则
sudo iptables -A INPUT -p tcp --dport 18081 -j ACCEPT

# 保存规则（根据系统不同）
# Ubuntu/Debian:
sudo netfilter-persistent save
# 或
sudo iptables-save > /etc/iptables/rules.v4

# CentOS/RHEL:
sudo service iptables save
```

### 3. 测试端口连通性

#### 从服务器本地测试

```bash
# 测试本地监听
curl -I http://127.0.0.1:18081

# 测试绑定到0.0.0.0的访问（使用服务器内网IP）
curl -I http://内网IP:18081
```

#### 从外部测试

```bash
# 使用telnet测试端口是否开放
telnet 你的公网IP 18081

# 或使用nc（netcat）
nc -zv 你的公网IP 18081

# 或使用curl从另一台机器
curl -I http://你的公网IP:18081
```

### 4. 检查Docker网络配置

虽然端口映射看起来正确，但可以验证一下：

```bash
# 检查Docker端口映射
docker-compose ps
docker port library-frontend 80

# 检查Docker网络
docker network inspect library_default | grep -A 10 frontend
```

### 5. 检查nginx配置

确认nginx监听所有接口：

```bash
# 进入容器检查nginx配置
docker exec library-frontend cat /etc/nginx/conf.d/default.conf | grep listen

# 应该看到：listen 80; 或 listen 0.0.0.0:80;
```

## 快速诊断脚本

创建一个诊断脚本来检查所有可能的问题：

```bash
#!/bin/bash
echo "=== 公网访问诊断 ==="
echo ""

echo "1. 检查Docker端口映射："
docker-compose ps | grep frontend
echo ""

echo "2. 检查端口监听状态："
ss -tlnp | grep 18081 || netstat -tlnp | grep 18081
echo ""

echo "3. 检查ufw状态："
sudo ufw status 2>/dev/null || echo "ufw未安装或未启用"
echo ""

echo "4. 检查iptables规则（需要sudo）："
sudo iptables -L INPUT -n -v | grep 18081 || echo "未找到18081相关规则"
echo ""

echo "5. 测试本地连接："
curl -I http://127.0.0.1:18081 2>&1 | head -3
echo ""

echo "6. 获取公网IP："
curl -s ifconfig.me || curl -s ipinfo.io/ip || echo "无法获取公网IP"
echo ""

echo "=== 诊断完成 ==="
echo ""
echo "如果本地访问正常但公网无法访问，最可能的原因是："
echo "1. 阿里云安全组未开放18081端口（最常见）"
echo "2. 服务器防火墙阻止了外部访问"
echo ""
echo "请按照上述步骤逐一检查。"
```

## 常见问题FAQ

### Q: 为什么本地可以访问但公网不行？

**A**: 这是典型的防火墙/安全组问题：
- 本地访问（127.0.0.1）不经过防火墙
- 公网访问需要经过：
  1. 阿里云安全组（最外层）
  2. 服务器防火墙（ufw/iptables）
  3. Docker端口映射（已确认正常）

### Q: 安全组配置后多久生效？

**A**: 通常立即生效，但建议等待1-2分钟。

### Q: 如何确认是安全组还是防火墙的问题？

**A**: 
- 如果telnet公网IP:18081连接超时 → 安全组问题
- 如果telnet能连接但curl失败 → 应用层问题
- 如果完全无法连接 → 检查安全组和防火墙

### Q: 可以只允许特定IP访问吗？

**A**: 可以，在安全组规则中：
- 授权对象改为：`你的IP/32`（单个IP）
- 或：`你的IP段/24`（IP段）

## 验证步骤

修复后，按以下顺序验证：

1. **检查安全组规则**（阿里云控制台）
2. **检查防火墙规则**（服务器上）
3. **测试端口连通性**（从外部机器）
4. **测试HTTP访问**（浏览器或curl）

## 安全建议

⚠️ **重要**：开放端口到公网前，请确保：
1. ✅ 已修改默认管理员密码
2. ✅ 已设置强SECRET_KEY
3. ✅ 已配置HTTPS（强烈推荐）
4. ✅ 已限制CORS来源
5. ✅ 已配置速率限制

参考：`docs/SECURITY_AUDIT.md`
