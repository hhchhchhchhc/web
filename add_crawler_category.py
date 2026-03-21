#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 1. 创建"爬虫"分类
category, created = Category.objects.get_or_create(
    name='爬虫',
    defaults={
        'description': '网页爬虫和数据采集工具'
    }
)

if created:
    print(f'✓ 已创建分类: {category.name}')
else:
    print(f'- 分类已存在: {category.name}')

print()
