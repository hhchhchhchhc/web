#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool

# 查找所有可能相关的工具
print('查找HappyCapy和知识星球相关工具...\n')

# 查找HappyCapy
happycapy_tools = Tool.objects.filter(name__icontains='HappyCapy')
print(f'=== HappyCapy工具 ===')
for tool in happycapy_tools:
    print(f'ID: {tool.id}')
    print(f'名称: {tool.name}')
    print(f'URL: {tool.website_url}')
    print(f'分类: {tool.category.name}')
    print(f'短描述: {tool.short_description[:50]}...')
    print()

# 查找知识星球工具
zsxq_tools = Tool.objects.filter(name__icontains='知识星球')
print(f'\n=== 知识星球工具 ===')
for tool in zsxq_tools:
    print(f'ID: {tool.id}')
    print(f'名称: {tool.name}')
    print(f'URL: {tool.website_url}')
    print(f'分类: {tool.category.name}')
    print(f'短描述: {tool.short_description[:50]}...')
    if 'DecompGRU' in tool.full_description:
        print(f'⚠️  包含DecompGRU描述')
    print()

# 查找所有包含DecompGRU的工具
print(f'\n=== 所有包含DecompGRU的工具 ===')
decompgru_tools = Tool.objects.filter(full_description__icontains='DecompGRU')
for tool in decompgru_tools:
    print(f'ID: {tool.id}')
    print(f'名称: {tool.name}')
    print(f'URL: {tool.website_url}')
    print(f'分类: {tool.category.name}')
    print()
