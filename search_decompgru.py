#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool

# 搜索包含特定描述的工具
search_text = "深度学习量化模型：提供名为 DecompGRU 的端到端模型源码"

print('搜索包含指定描述的工具...\n')

# 搜索short_description和full_description
tools = Tool.objects.filter(
    short_description__icontains='DecompGRU'
) | Tool.objects.filter(
    full_description__icontains='DecompGRU'
)

found_tools = []
for tool in tools:
    found_tools.append(tool)
    print(f'找到: {tool.name}')
    print(f'  短描述: {tool.short_description}')
    print(f'  完整描述: {tool.full_description[:100]}...')
    print(f'  URL: {tool.website_url}')
    print(f'  分类: {tool.category.name}')
    print()

if found_tools:
    print(f'\n共找到 {len(found_tools)} 个相关工具')
else:
    print('未找到相关工具')
