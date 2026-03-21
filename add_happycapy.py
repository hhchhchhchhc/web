#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 工具数据
tool_data = {
    'name': 'HappyCapy',
    'short_description': '无限注册账号免费使用顶级AI模型',
    'full_description': 'HappyCapy是一个可以通过注册多个账号来免费使用顶级AI大模型的平台。支持无限注册，让用户能够持续免费访问最先进的AI模型服务。',
    'website_url': 'https://happycapy.ai/app',
    'category_name': '免费用最高级大模型'
}

# 添加工具
try:
    category = Category.objects.get(name=tool_data['category_name'])

    tool, created = Tool.objects.get_or_create(
        name=tool_data['name'],
        defaults={
            'short_description': tool_data['short_description'],
            'full_description': tool_data['full_description'],
            'website_url': tool_data['website_url'],
            'category': category
        }
    )

    if created:
        print(f'✓ 已添加: {tool.name} → {category.name}')
        print(f'  URL: {tool.website_url}')
    else:
        print(f'- 工具已存在: {tool.name}')
        print(f'  当前URL: {tool.website_url}')
except Category.DoesNotExist:
    print(f'✗ 分类不存在: {tool_data["category_name"]}')
except Exception as e:
    print(f'✗ 添加失败: {e}')
