#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool

# 查找slug为happycapy的工具
print('=== 查找slug为happycapy的工具 ===')
try:
    tool = Tool.objects.get(slug='happycapy')
    print(f'ID: {tool.id}')
    print(f'名称: {tool.name}')
    print(f'Slug: {tool.slug}')
    print(f'URL: {tool.website_url}')
    print(f'分类: {tool.category.name}')
    print(f'\n短描述:')
    print(tool.short_description)
    print(f'\n完整描述（前200字符）:')
    print(tool.full_description[:200])

    if 'DecompGRU' in tool.full_description:
        print(f'\n⚠️  此工具包含DecompGRU描述！')
except Tool.DoesNotExist:
    print('未找到slug为happycapy的工具')

# 查找名称为HappyCapy的工具
print('\n\n=== 查找名称为HappyCapy的工具 ===')
happycapy_tools = Tool.objects.filter(name='HappyCapy')
for tool in happycapy_tools:
    print(f'ID: {tool.id}')
    print(f'名称: {tool.name}')
    print(f'Slug: {tool.slug}')
    print(f'URL: {tool.website_url}')
