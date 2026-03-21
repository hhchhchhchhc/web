#!/usr/bin/env python3
import os
import django
from collections import defaultdict

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

categories = Category.objects.all()

for cat in categories:
    tools = cat.tools.all()[:50]  # 取前50个样本
    print(f'\n{"="*60}')
    print(f'{cat.name} ({cat.tools.count()} 个工具)')
    print(f'{"="*60}')

    for i, tool in enumerate(tools, 1):
        print(f'{i}. {tool.name} - {tool.website_url[:60]}')

    if cat.tools.count() > 50:
        print(f'... 还有 {cat.tools.count() - 50} 个工具')
