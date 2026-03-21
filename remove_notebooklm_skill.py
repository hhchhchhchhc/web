#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool

tool = Tool.objects.filter(name='Anything to NotebookLM').first()
if tool:
    tool.delete()
    print("✅ Anything to NotebookLM工具已删除！")
else:
    print("❌ 未找到该工具")
