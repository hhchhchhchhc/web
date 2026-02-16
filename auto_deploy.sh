#!/bin/bash
# 一键自动部署脚本 - 完全自动化
# 使用方法: curl -sSL https://raw.githubusercontent.com/hhchhchhchhc/web/main/auto_deploy.sh | sudo bash

set -e

echo "=========================================="
echo "Django 工具聚合网站 - 一键自动部署"
echo "=========================================="
echo ""

# 检查是否以 root 运行
if [ "$EUID" -ne 0 ]; then
    echo "❌ 请使用 sudo 运行此脚本"
    exit 1
fi

# 配置变量
DOMAIN="hanchihuang.indevs.in"
APP_NAME="tool_aggregator"
APP_USER="www-data"
APP_DIR="/var/www/$APP_NAME"
VENV_DIR="$APP_DIR/venv"
REPO_URL="https://github.com/hhchhchhchhc/web.git"

echo "📦 步骤 1/10: 更新系统"
echo "----------------------------------------"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get upgrade -y -qq

echo ""
echo "📦 步骤 2/10: 安装依赖包"
echo "----------------------------------------"
apt-get install -y -qq \
    python3 \
    python3-pip \
    python3-venv \
    postgresql \
    postgresql-contrib \
    nginx \
    git \
    certbot \
    python3-certbot-nginx \
    ufw

echo "✅ 依赖包安装完成"
echo ""

echo "🔒 步骤 3/10: 配置防火墙"
echo "----------------------------------------"
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
echo "✅ 防火墙配置完成"
echo ""

echo "🗄️ 步骤 4/10: 创建 PostgreSQL 数据库"
echo "----------------------------------------"
DB_PASSWORD=$(openssl rand -base64 32)
sudo -u postgres psql -c "DROP DATABASE IF EXISTS tool_aggregator_db;" 2>/dev/null || true
sudo -u postgres psql -c "DROP USER IF EXISTS tool_aggregator_user;" 2>/dev/null || true
sudo -u postgres psql <<EOF
CREATE DATABASE tool_aggregator_db;
CREATE USER tool_aggregator_user WITH PASSWORD '$DB_PASSWORD';
ALTER ROLE tool_aggregator_user SET client_encoding TO 'utf8';
ALTER ROLE tool_aggregator_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE tool_aggregator_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE tool_aggregator_db TO tool_aggregator_user;
EOF

echo "✅ 数据库创建成功"
echo ""

echo "📁 步骤 5/10: 准备应用目录"
echo "----------------------------------------"
rm -rf $APP_DIR
mkdir -p $APP_DIR
cd $APP_DIR

echo ""
echo "📥 步骤 6/10: 克隆代码"
echo "----------------------------------------"
git clone $REPO_URL code
cd code

echo ""
echo "🐍 步骤 7/10: 配置 Python 环境"
echo "----------------------------------------"
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo "✅ Python 环境配置完成"
echo ""

echo "⚙️ 步骤 8/10: 配置环境变量"
echo "----------------------------------------"
SECRET_KEY=$(python3 -c "import secrets; print(''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(50)))")

cat > $APP_DIR/.env <<EOF
DJANGO_SETTINGS_MODULE=config.settings_prod
SECRET_KEY=$SECRET_KEY
DATABASE_URL=postgresql://tool_aggregator_user:$DB_PASSWORD@localhost/tool_aggregator_db
ALLOWED_HOSTS=$DOMAIN
DEBUG=False
EOF

echo "✅ 环境变量配置完成"
echo ""

echo "🔄 步骤 9/10: 初始化数据库"
echo "----------------------------------------"
cd $APP_DIR/code
source $VENV_DIR/bin/activate
export $(cat $APP_DIR/.env | xargs)
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "✅ 数据库初始化完成"
echo ""

echo "🔧 步骤 10/10: 配置服务"
echo "----------------------------------------"

# 创建日志目录
mkdir -p /var/log/gunicorn
chown -R $APP_USER:$APP_USER /var/log/gunicorn

# 配置 Gunicorn 服务
cat > /etc/systemd/system/gunicorn.service <<EOF
[Unit]
Description=Gunicorn daemon for Django Tool Aggregator
After=network.target

[Service]
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR/code
EnvironmentFile=$APP_DIR/.env
ExecStart=$VENV_DIR/bin/gunicorn \\
    --workers 3 \\
    --bind unix:$APP_DIR/gunicorn.sock \\
    --timeout 120 \\
    --access-logfile /var/log/gunicorn/access.log \\
    --error-logfile /var/log/gunicorn/error.log \\
    config.wsgi:application

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# 配置 Nginx
cat > /etc/nginx/sites-available/$APP_NAME <<EOF
server {
    listen 80;
    server_name $DOMAIN;

    client_max_body_size 10M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias $APP_DIR/code/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias $APP_DIR/code/media/;
        expires 7d;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$APP_DIR/gunicorn.sock;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header Host \$host;
        proxy_redirect off;
    }
}
EOF

# 启用 Nginx 配置
ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 设置文件权限
chown -R $APP_USER:$APP_USER $APP_DIR

# 启动服务
systemctl daemon-reload
systemctl start gunicorn
systemctl enable gunicorn
systemctl restart nginx

echo "✅ 服务配置完成"
echo ""

# 检查服务状态
if systemctl is-active --quiet gunicorn; then
    echo "✅ Gunicorn 服务运行正常"
else
    echo "❌ Gunicorn 服务启动失败"
    systemctl status gunicorn
fi

if systemctl is-active --quiet nginx; then
    echo "✅ Nginx 服务运行正常"
else
    echo "❌ Nginx 服务启动失败"
    systemctl status nginx
fi

echo ""
echo "=========================================="
echo "🎉 部署完成！"
echo "=========================================="
echo ""
echo "📝 重要信息："
echo "----------------------------------------"
echo "域名: $DOMAIN"
echo "应用目录: $APP_DIR"
echo "数据库密码已保存到: $APP_DIR/.env"
echo ""
echo "📋 下一步操作："
echo "----------------------------------------"
echo "1. 配置域名 DNS："
echo "   - 登录域名管理面板"
echo "   - 添加 A 记录: hanchihuang -> VPS公网IP"
echo "   - 等待 DNS 生效（5-30分钟）"
echo ""
echo "2. 配置 SSL 证书（DNS 生效后）："
echo "   sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email qqhuanghanchi@gmail.com"
echo ""
echo "3. 创建管理员账号："
echo "   cd $APP_DIR/code"
echo "   sudo -u $APP_USER $VENV_DIR/bin/python manage.py createsuperuser"
echo ""
echo "4. 访问网站："
echo "   http://$DOMAIN (DNS 生效后)"
echo ""
echo "🔧 常用命令："
echo "----------------------------------------"
echo "查看服务状态: sudo systemctl status gunicorn"
echo "重启服务: sudo systemctl restart gunicorn"
echo "查看日志: sudo journalctl -u gunicorn -f"
echo ""
