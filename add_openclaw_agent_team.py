#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category = Category.objects.get(name='openclaw使用方法')

tool_data = {
    'name': '快过年了，让我们来组个你自己的Agent团队吧',
    'short_description': 'OpenClaw Agent团队搭建教程，教你组建自己的AI Agent团队',
    'full_description': 'OpenClaw实战教程，详细讲解如何使用OpenClaw搭建和管理自己的AI Agent团队。从基础配置到团队协作，帮助你快速上手Agent团队的组建和使用。',
    'website_url': 'https://my.feishu.cn/wiki/EDYWw2mPniwGGLk8r6wcMmpXnZc?from=from_copylink'
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
