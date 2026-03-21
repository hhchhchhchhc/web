#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool

# 搜索可能的工具名称
search_terms = ['讯飞', 'iFlytek', 'AI学习平台', '科大讯飞']

print('搜索相关工具...\n')
found_tools = []

for term in search_terms:
    tools = Tool.objects.filter(name__icontains=term) | Tool.objects.filter(short_description__icontains=term) | Tool.objects.filter(full_description__icontains=term)
    for tool in tools:
        if tool not in found_tools:
            found_tools.append(tool)
            print(f'找到: {tool.name}')
            print(f'  描述: {tool.short_description}')
            print(f'  URL: {tool.website_url}')
            print(f'  分类: {tool.category.name}')
            print()

if found_tools:
    print(f'\n共找到 {len(found_tools)} 个相关工具')
    print('\n是否删除这些工具? 请手动确认后运行删除命令')
else:
    print('未找到相关工具')
