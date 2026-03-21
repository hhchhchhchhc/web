#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool

# 查找HappyCapy工具
try:
    tool = Tool.objects.get(name='HappyCapy')
    print(f'工具名称: {tool.name}')
    print(f'分类: {tool.category.name}')
    print(f'URL: {tool.website_url}')
    print(f'\n短描述:')
    print(tool.short_description)
    print(f'\n完整描述:')
    print(tool.full_description)
    print(f'\n描述长度: {len(tool.full_description)} 字符')

    # 检查是否包含DecompGRU
    if 'DecompGRU' in tool.short_description or 'DecompGRU' in tool.full_description:
        print(f'\n⚠️  发现DecompGRU描述！')
    else:
        print(f'\n✓ 未发现DecompGRU描述')

except Tool.DoesNotExist:
    print('✗ 未找到HappyCapy工具')
except Exception as e:
    print(f'✗ 查询失败: {e}')
