#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# Create category if it doesn't exist
category, created = Category.objects.get_or_create(
    name='openclaw使用方法',
    defaults={'description': 'OpenClaw AI工具使用教程和实践经验'}
)

if created:
    print(f'✓ 已创建分类: {category.name}')
else:
    print(f'- 分类已存在: {category.name}')

# Add tool
tool_data = {
    'name': '半个月烧了500美金，把OpenClaw折腾成真干活的AI员工',
    'short_description': 'OpenClaw实战经验分享，从零到一打造真正能干活的AI员工',
    'full_description': '作者分享了半个月时间、花费500美金将OpenClaw调教成真正能干活的AI员工的实战经验。详细记录了配置过程、踩坑经验和实用技巧，帮助你快速上手OpenClaw。',
    'website_url': 'https://zi6nfl20s5u.feishu.cn/wiki/JEF7wyBfzigEthkYwJfcy1I0n9b'
}

tool, created = Tool.objects.get_or_create(
    name=tool_data['name'],
    defaults={
        **tool_data,
        'category': category
    }
)

if created:
    print(f'✓ 已添加: {tool.name} → {category.name}')
else:
    print(f'- 已存在: {tool.name}')

print('\n完成！')
