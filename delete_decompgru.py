#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool

# 删除包含DecompGRU描述的工具
print('正在删除包含DecompGRU描述的工具...\n')

# 搜索并删除
tools = Tool.objects.filter(
    short_description__icontains='DecompGRU'
) | Tool.objects.filter(
    full_description__icontains='DecompGRU'
)

deleted_count = 0
for tool in tools:
    tool_name = tool.name
    tool_url = tool.website_url
    tool.delete()
    deleted_count += 1
    print(f'✓ 已删除: {tool_name}')
    print(f'  URL: {tool_url}')
    print()

if deleted_count > 0:
    print(f'\n总共删除了 {deleted_count} 个工具')
else:
    print('未找到需要删除的工具')
