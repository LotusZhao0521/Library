# 公网部署安全审计报告

**审计日期**: 2026-02-08  
**项目**: 图书管理系统  
**部署环境**: 公网部署

## 🔴 严重安全问题（必须立即修复）

### 1. 弱密钥和默认密码
**风险等级**: 🔴 严重

**问题**:
- `SECRET_KEY` 使用弱默认值：`"change-me-in-production"` 或 `"library-secret-key-change-in-production"`
- 管理员默认密码：`admin123`（弱密码）
- 默认管理员用户名：`admin`（容易被猜测）

**影响**:
- JWT token 可以被伪造
- 攻击者可以获取管理员权限
- 系统完全暴露

**修复建议**:
```bash
# 在 backend/.env 中设置强密钥（至少32字符随机字符串）
SECRET_KEY=$(openssl rand -hex 32)

# 设置强管理员密码（至少12字符，包含大小写字母、数字、特殊字符）
ADMIN_PASSWORD=<强密码>

# 修改默认管理员用户名
ADMIN_USERNAME=<自定义用户名>
```

### 2. CORS 配置过于宽松
**风险等级**: 🔴 严重

**问题**:
```python
# backend/app/main.py:38
allow_origins=["*"]  # 允许所有来源
```

**影响**:
- 任何网站都可以调用你的API
- 容易受到CSRF攻击
- 敏感数据可能被恶意网站窃取

**修复建议**:
```python
# 生产环境应该限制为前端域名
allow_origins=[
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
# 或者至少限制为特定IP
allow_origins=["http://你的公网IP:18081"]
```

### 3. 缺少HTTPS/TLS加密
**风险等级**: 🔴 严重

**问题**:
- 当前配置仅支持HTTP
- 所有数据传输未加密
- 密码、token等敏感信息明文传输

**影响**:
- 中间人攻击可以窃取所有数据
- 密码和token可以被拦截
- 违反数据保护法规

**修复建议**:
- 使用反向代理（Nginx/Caddy）配置SSL证书
- 使用Let's Encrypt免费证书
- 强制HTTPS重定向
- 配置HSTS头

### 4. 后端端口直接暴露
**风险等级**: 🟡 中等（如果仅内网访问则为低）

**问题**:
```yaml
# docker-compose.yml:8-9
ports:
  - "${PORT:-8000}:${PORT:-8000}"
```

**影响**:
- 如果防火墙配置不当，后端API可能直接暴露
- 绕过前端直接访问API

**修复建议**:
- 确保防火墙只开放前端端口（18081）
- 后端端口不应映射到公网，或使用Docker内部网络
- 修改docker-compose.yml，移除后端端口映射或仅映射到127.0.0.1

## 🟡 中等安全问题（建议尽快修复）

### 5. 缺少速率限制（Rate Limiting）
**风险等级**: 🟡 中等

**问题**:
- 没有API请求频率限制
- 登录接口没有防暴力破解保护

**影响**:
- 容易受到暴力破解攻击
- DDoS攻击风险
- 资源耗尽

**修复建议**:
- 安装 `slowapi` 或 `fastapi-limiter`
- 对登录接口限制：5次/分钟
- 对API接口限制：100次/分钟/IP

### 6. Token过期时间过长
**风险等级**: 🟡 中等

**问题**:
```python
# backend/app/core/config.py:11
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24小时
```

**影响**:
- Token泄露后长期有效
- 无法及时撤销访问权限

**修复建议**:
- 缩短为2-4小时
- 实现refresh token机制
- 添加token撤销功能

### 7. 缺少安全响应头
**风险等级**: 🟡 中等

**问题**:
- 没有设置安全相关的HTTP头
- 缺少XSS保护、点击劫持保护等

**修复建议**:
在FastAPI中添加中间件设置安全头：
```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

# 生产环境强制HTTPS
app.add_middleware(HTTPSRedirectMiddleware)

# 添加安全头
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

### 8. 输入验证不够严格
**风险等级**: 🟡 中等

**问题**:
- 用户名、密码没有长度和复杂度验证
- Role字段没有枚举验证

**修复建议**:
```python
from pydantic import BaseModel, Field, field_validator
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    password: str = Field(..., min_length=8, max_length=100)
    role: UserRole = UserRole.USER
    
    @field_validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('密码必须包含至少一个大写字母')
        if not any(c.islower() for c in v):
            raise ValueError('密码必须包含至少一个小写字母')
        if not any(c.isdigit() for c in v):
            raise ValueError('密码必须包含至少一个数字')
        return v
```

### 9. 缺少日志和监控
**风险等级**: 🟡 中等

**问题**:
- 没有记录安全相关事件（登录失败、权限拒绝等）
- 没有异常监控和告警

**修复建议**:
- 记录所有登录尝试（成功/失败）
- 记录权限拒绝事件
- 记录异常请求
- 集成监控系统（如Sentry）

## 🟢 已实现的安全措施（良好）

✅ **密码哈希**: 使用bcrypt进行密码哈希  
✅ **JWT认证**: 使用JWT进行身份验证  
✅ **权限控制**: 实现了基本的admin/user角色控制  
✅ **SQL注入防护**: 使用SQLAlchemy ORM防止SQL注入  
✅ **环境变量隔离**: .env文件已正确忽略，不会提交到git  
✅ **Docker隔离**: 使用容器化部署，提供一定隔离

## 📋 部署前安全检查清单

在公网部署前，请确保完成以下所有项目：

### 必须完成（🔴）
- [ ] 修改 `SECRET_KEY` 为强随机字符串（至少32字符）
- [ ] 修改 `ADMIN_PASSWORD` 为强密码（至少12字符）
- [ ] 修改 `ADMIN_USERNAME` 为不易猜测的用户名
- [ ] 配置HTTPS/SSL证书
- [ ] 限制CORS为前端域名
- [ ] 确保防火墙只开放必要端口
- [ ] 验证后端端口不直接暴露到公网

### 强烈建议（🟡）
- [ ] 实现API速率限制
- [ ] 缩短Token过期时间
- [ ] 添加安全响应头
- [ ] 加强输入验证
- [ ] 配置日志记录
- [ ] 设置监控和告警

### 可选但推荐（🟢）
- [ ] 实现refresh token机制
- [ ] 添加双因素认证（2FA）
- [ ] 配置WAF（Web应用防火墙）
- [ ] 定期安全扫描
- [ ] 备份策略
- [ ] 灾难恢复计划

## 🚀 快速修复指南

### 1. 立即修复密钥和密码

```bash
# 生成强SECRET_KEY
openssl rand -hex 32

# 编辑 backend/.env
vim backend/.env

# 设置：
SECRET_KEY=<生成的强密钥>
ADMIN_USERNAME=<自定义用户名>
ADMIN_PASSWORD=<强密码>
```

### 2. 配置HTTPS（使用Caddy，最简单）

```dockerfile
# 创建 Caddyfile
echo 'yourdomain.com {
    reverse_proxy localhost:18081
    encode gzip
}' > Caddyfile

# 使用Caddy自动获取SSL证书
docker run -d \
  --name caddy \
  -p 80:80 -p 443:443 \
  -v $(pwd)/Caddyfile:/etc/caddy/Caddyfile \
  -v caddy_data:/data \
  caddy:latest
```

### 3. 限制CORS

编辑 `backend/app/main.py`:
```python
import os

# 从环境变量读取允许的来源
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
if not allowed_origins or allowed_origins == [""]:
    allowed_origins = ["*"]  # 开发环境

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

在 `backend/.env` 中添加：
```
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## 📚 参考资源

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security Best Practices](https://fastapi.tiangolo.com/tutorial/security/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)

---

**总结**: 当前项目**不适合直接公网部署**。必须至少修复所有🔴严重问题后才能考虑部署。建议完成🟡中等问题的修复以确保基本安全。
