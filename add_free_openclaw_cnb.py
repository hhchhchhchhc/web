#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category = Category.objects.get(name='openclaw使用方法')

tool_data = {
    'name': '免费OpenClaw一键启动 - 腾讯CNB',
    'short_description': '腾讯CNB代码托管平台，fork即可一键启动OpenClaw，大模型key自动配置',
    'full_description': '通过腾讯CNB代码托管平台免费使用OpenClaw，只需fork克隆仓库即可一键启动。平台已自动配置好大模型API key，无需额外配置，打开就能直接使用，零成本体验OpenClaw。',
    'website_url': 'https://cnb.cool/Bring/AGI/Moltbot-Clawdbot-OpenClaw/'
}

tool, created = Tool.objects.get_or_create(
    name=tool_data['name'],
    defaults={
        **tool_data,
        'category': category
    }
)

if created:
    print(f'✓ 已添加: {tool.name} → {category.name}')
else:
    print(f'- 已存在: {tool.name}')

print('\n完成！')
