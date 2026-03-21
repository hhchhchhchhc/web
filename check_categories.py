import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 查找这两个分类
categories = Category.objects.filter(name__in=['副业赚钱', '赚钱技巧'])

for cat in categories:
    print(f'\n分类: {cat.name} (ID: {cat.id})')
    print(f'描述: {cat.description}')
    print(f'顺序: {cat.order}')
    tools = Tool.objects.filter(category=cat)
    print(f'工具数量: {tools.count()}')
    for tool in tools:
        print(f'  - {tool.name}')
