#!/usr/bin/env python
"""删除没有工具的空分类"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db.models import Count
from tools.models import Category

# 查找并删除空分类
empty_categories = Category.objects.annotate(
    tool_count=Count('tools')
).filter(tool_count=0)

count = empty_categories.count()
print(f'找到 {count} 个空分类')

if input('确认删除？(y/n): ').lower() == 'y':
    empty_categories.delete()
    print(f'已删除 {count} 个空分类')
