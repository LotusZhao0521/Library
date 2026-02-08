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

echo "4. 测试本地连接："
curl -I http://127.0.0.1:18081 2>&1 | head -3
echo ""

echo "5. 获取公网IP："
curl -s ifconfig.me 2>/dev/null || curl -s ipinfo.io/ip 2>/dev/null || echo "无法获取公网IP"
echo ""

echo "=== 诊断完成 ==="
echo ""
echo "如果本地访问正常但公网无法访问，最可能的原因是："
echo "1. 🔴 阿里云安全组未开放18081端口（最常见）"
echo "2. 🟡 服务器防火墙（ufw/iptables）阻止了外部访问"
echo ""
echo "详细解决方案请查看：docs/PUBLIC_ACCESS_TROUBLESHOOTING.md"
