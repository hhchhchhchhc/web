#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category, _ = Category.objects.get_or_create(
    name='免费用最高级大模型',
    defaults={'description': '免费使用顶级AI大模型的平台', 'order': 3}
)

tool = Tool.objects.get(slug='cto-new')
tool.category = category
tool.save()

print('✓ 已将 CTO.NEW 移动到"免费用最高级大模型"分类')
