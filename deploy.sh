#!/bin/bash

# 自动化部署脚本
# 使用方法: ./deploy.sh

set -e  # 遇到错误立即退出

echo "=========================================="
echo "工具聚合网站自动化部署脚本"
echo "=========================================="
echo ""

# 检查是否在正确的目录
if [ ! -f "manage.py" ]; then
    echo "错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 步骤1: 推送到GitHub
echo "步骤 1/3: 推送代码到 GitHub"
echo "----------------------------------------"

# 检查是否已经配置了remote
if git remote | grep -q "origin"; then
    echo "✓ Git remote 已配置"
    REPO_URL=$(git remote get-url origin)
    echo "  仓库地址: $REPO_URL"
else
    echo "请输入你的 GitHub 仓库 URL (例如: https://github.com/username/tool_aggregator.git):"
    read REPO_URL

    if [ -z "$REPO_URL" ]; then
        echo "错误: 仓库 URL 不能为空"
        exit 1
    fi

    echo "正在添加 remote..."
    git remote add origin "$REPO_URL"
    echo "✓ Remote 添加成功"
fi

# 推送代码
echo "正在推送代码到 GitHub..."
git branch -M main
git push -u origin main --force

echo "✓ 代码已推送到 GitHub"
echo ""

# 步骤2: 生成部署信息
echo "步骤 2/3: 生成部署配置"
echo "----------------------------------------"

# 生成SECRET_KEY
SECRET_KEY=$(python3 -c "import secrets; print(''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#\$%^&*(-_=+)') for i in range(50)))")

echo "✓ 已生成 SECRET_KEY"
echo ""

# 步骤3: 显示Railway部署说明
echo "步骤 3/3: Railway 部署说明"
echo "----------------------------------------"
echo ""
echo "代码已推送到 GitHub，现在需要在 Railway 上部署："
echo ""
echo "1. 访问 https://railway.app"
echo "2. 使用 GitHub 登录"
echo "3. 点击 'New Project' → 'Deploy from GitHub repo'"
echo "4. 选择你的仓库: $(basename $REPO_URL .git)"
echo "5. 添加 PostgreSQL 数据库: 点击 'New' → 'Database' → 'PostgreSQL'"
echo "6. 配置环境变量 (在 Variables 标签):"
echo ""
echo "   DJANGO_SETTINGS_MODULE=config.settings_prod"
echo "   SECRET_KEY=$SECRET_KEY"
echo "   ALLOWED_HOSTS=*.railway.app,你的域名.com"
echo "   DEBUG=False"
echo ""
echo "7. 等待部署完成"
echo "8. 创建超级用户:"
echo "   railway run python manage.py createsuperuser"
echo ""
echo "=========================================="
echo "部署配置已保存到 deployment_info.txt"
echo "=========================================="

# 保存部署信息到文件
cat > deployment_info.txt << EOF
# Railway 部署配置信息
# 生成时间: $(date)

## GitHub 仓库
$REPO_URL

## 环境变量配置
DJANGO_SETTINGS_MODULE=config.settings_prod
SECRET_KEY=$SECRET_KEY
ALLOWED_HOSTS=*.railway.app,你的域名.com
DEBUG=False

## Railway 部署步骤
1. 访问 https://railway.app
2. 使用 GitHub 登录
3. 点击 'New Project' → 'Deploy from GitHub repo'
4. 选择仓库: $(basename $REPO_URL .git)
5. 添加 PostgreSQL: 'New' → 'Database' → 'PostgreSQL'
6. 配置上述环境变量
7. 等待部署完成
8. 创建超级用户: railway run python manage.py createsuperuser

## 域名配置
在 Railway 项目中添加自定义域名，然后在域名提供商配置 CNAME 记录
EOF

echo ""
echo "✓ 完成！请按照上述说明在 Railway 上完成部署"
