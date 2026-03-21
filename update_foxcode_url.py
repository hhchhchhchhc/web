#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool

# 更新FoxCode的URL
try:
    foxcode = Tool.objects.get(name='FoxCode')
    old_url = foxcode.website_url
    foxcode.website_url = 'https://foxcode.rjj.cc/auth/register?aff=G6Z4FV5G'
    foxcode.save()
    print(f'✓ 已更新FoxCode URL')
    print(f'  旧URL: {old_url}')
    print(f'  新URL: {foxcode.website_url}')
except Tool.DoesNotExist:
    print('✗ 未找到FoxCode工具')
except Exception as e:
    print(f'✗ 更新失败: {e}')
