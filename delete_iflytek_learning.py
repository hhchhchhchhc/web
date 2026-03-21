#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool

# 删除指定工具
try:
    tool = Tool.objects.get(name='科大讯飞推出的在线AI学习平台')
    tool_name = tool.name
    tool_url = tool.website_url
    tool.delete()
    print(f'✓ 已删除工具: {tool_name}')
    print(f'  URL: {tool_url}')
except Tool.DoesNotExist:
    print('✗ 未找到该工具')
except Exception as e:
    print(f'✗ 删除失败: {e}')
