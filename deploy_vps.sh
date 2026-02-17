#!/bin/bash
# VPS 自动化部署脚本
# 使用方法: sudo bash deploy_vps.sh

set -e

echo "=========================================="
echo "Django 工具聚合网站 VPS 部署脚本"
echo "=========================================="
echo ""

# 检查是否以 root 运行
if [ "$EUID" -ne 0 ]; then
    echo "请使用 sudo 运行此脚本"
    exit 1
fi

# 配置变量
DOMAIN="hanchihuang.indevs.in"
APP_NAME="tool_aggregator"
APP_USER="www-data"
APP_DIR="/var/www/$APP_NAME"
VENV_DIR="$APP_DIR/venv"

echo "步骤 1/8: 更新系统并安装依赖"
echo "----------------------------------------"
apt-get update
apt-get install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git

echo ""
echo "步骤 2/8: 创建 PostgreSQL 数据库"
echo "----------------------------------------"
DB_PASSWORD=$(openssl rand -base64 32)
sudo -u postgres psql <<EOF
CREATE DATABASE tool_aggregator_db;
CREATE USER tool_aggregator_user WITH PASSWORD '$DB_PASSWORD';
ALTER ROLE tool_aggregator_user SET client_encoding TO 'utf8';
ALTER ROLE tool_aggregator_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE tool_aggregator_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE tool_aggregator_db TO tool_aggregator_user;
\q
EOF

echo "数据库创建成功！"
echo "数据库密码: $DB_PASSWORD"
echo ""

echo "步骤 3/8: 创建应用目录"
echo "----------------------------------------"
mkdir -p $APP_DIR
cd $APP_DIR

echo ""
echo "步骤 4/8: 克隆代码"
echo "----------------------------------------"
if [ -d "$APP_DIR/code" ]; then
    rm -rf $APP_DIR/code
fi
git clone https://github.com/hhchhchhchhc/web.git code
cd code

echo ""
echo "步骤 5/8: 创建虚拟环境并安装依赖"
echo "----------------------------------------"
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "步骤 6/8: 配置环境变量"
echo "----------------------------------------"
SECRET_KEY=$(python3 -c "import secrets; print(''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#\$%^&*(-_=+)') for i in range(50)))")

cat > $APP_DIR/.env <<EOF
DJANGO_SETTINGS_MODULE=config.settings_prod
SECRET_KEY=$SECRET_KEY
DATABASE_URL=postgresql://tool_aggregator_user:$DB_PASSWORD@localhost/tool_aggregator_db
ALLOWED_HOSTS=$DOMAIN
DEBUG=False
EOF

echo "环境变量配置完成"
echo ""

echo "步骤 7/8: 运行数据库迁移和收集静态文件"
echo "----------------------------------------"
cd $APP_DIR/code
source $VENV_DIR/bin/activate
export $(cat $APP_DIR/.env | xargs)
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo ""
echo "步骤 8/8: 设置文件权限"
echo "----------------------------------------"
chown -R $APP_USER:$APP_USER $APP_DIR

echo ""
echo "=========================================="
echo "部署完成！"
echo "=========================================="
echo ""
echo "数据库信息已保存到: $APP_DIR/.env"
echo ""
echo "下一步："
echo "1. 配置 Gunicorn 服务"
echo "2. 配置 Nginx"
echo "3. 配置 SSL 证书"
echo "4. 创建超级用户"
echo ""
