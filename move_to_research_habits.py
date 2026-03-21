#!/usr/bin/env python
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# Create new category
category, created = Category.objects.get_or_create(
    name='研究习惯',
    defaults={'slug': slugify('研究习惯', allow_unicode=True)}
)

if created:
    print("✅ 已创建新分类：研究习惯")
else:
    print("ℹ️  分类已存在：研究习惯")

# Move the video speed tip to this category
tool = Tool.objects.get(slug='ai-video-speed-watching')
tool.category = category
tool.save()

print("✅ 已将'AI加速看视频方法'移动到'研究习惯'分类")
