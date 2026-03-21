#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool

tool = Tool.objects.get(slug='cto-new')
tool.short_description = '永久免费使用GPT-5.2、Claude opus 4.5、Gemini 3 Pro等当前基本上最顶级AI模型'
tool.save()

print('✓ 已更新：CTO.NEW 描述信息')
