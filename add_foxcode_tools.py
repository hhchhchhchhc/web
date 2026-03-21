#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 工具数据
tools_data = [
    {
        'name': 'FoxCode',
        'short_description': 'AWS逆向渠道Claude API服务，支持200k上下文和缓存功能',
        'full_description': 'FoxCode是一个提供Claude API服务的平台，通过AWS逆向渠道提供稳定的Claude服务。支持200k满血上下文、缓存功能、Web联网搜索能力。价格低至三分钱，性价比极高。',
        'website_url': 'https://foxcode.rjj.cc/',
        'category_name': 'AI编程工具'
    },
    {
        'name': 'Kiro',
        'short_description': '免费使用Claude Opus的工具，支持多账号无限使用',
        'full_description': 'Kiro是一个可以免费使用Claude Opus的工具，支持开多个号无限免费使用。提供稳定的Claude Opus访问能力。',
        'website_url': 'https://kiro.ai/',
        'category_name': '免费用最高级大模型'
    },
    {
        'name': 'Planning with Files',
        'short_description': 'Claude Code的文件规划Skill，提升AI编程精准度',
        'full_description': 'Planning with Files是一个用于Claude Code的Skill工具，实现Manus风格的基于文件的规划功能。能够精准回答问题，提升AI编程体验。',
        'website_url': 'https://github.com/OthmanAdi/planning-with-files',
        'category_name': 'AI编程工具'
    }
]

# 添加工具
for tool_data in tools_data:
    category_name = tool_data.pop('category_name')
    category = Category.objects.get(name=category_name)

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
