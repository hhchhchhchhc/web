#!/usr/bin/env python
import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool

# 要删除的文本模式
decompgru_patterns = [
    r'深度学习量化模型：提供名为\s*DecompGRU\s*的端到端模型源码（基于趋势分解\s*的时序\+截面模型），据称效果惊人',
    r'深度学习量化模型.*?DecompGRU.*?据称效果惊人',
    r'- 深度学习量化模型.*?DecompGRU.*?\n',
    r'\n.*?DecompGRU.*?据称效果惊人.*?\n',
]

print('搜索包含DecompGRU描述的所有工具...\n')

# 搜索所有包含DecompGRU的工具
tools = Tool.objects.filter(
    short_description__icontains='DecompGRU'
) | Tool.objects.filter(
    full_description__icontains='DecompGRU'
)

found_count = 0
for tool in tools:
    found_count += 1
    print(f'找到工具 #{found_count}: {tool.name}')
    print(f'  分类: {tool.category.name}')
    print(f'  URL: {tool.website_url}')

    # 检查short_description
    if 'DecompGRU' in tool.short_description:
        print(f'  ⚠️  短描述包含DecompGRU')
        print(f'     原文: {tool.short_description[:100]}...')

    # 检查full_description
    if 'DecompGRU' in tool.full_description:
        print(f'  ⚠️  完整描述包含DecompGRU')
        # 显示包含DecompGRU的行
        lines = tool.full_description.split('\n')
        for i, line in enumerate(lines):
            if 'DecompGRU' in line:
                print(f'     第{i+1}行: {line.strip()[:100]}...')

    print()

print(f'\n总共找到 {found_count} 个包含DecompGRU的工具')
