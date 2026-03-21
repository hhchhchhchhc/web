#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 获取或创建分类
free_cat, _ = Category.objects.get_or_create(
    name='免费用最高级大模型',
    defaults={
        'slug': slugify('免费用最高级大模型', allow_unicode=True),
        'description': '免费使用Claude Opus 4.6等顶级AI模型的方法'
    }
)

# 添加Web IDE工具
full_desc = """免费开源的Web IDE，可以使用Opus 4.6

安装命令：
• Windows: irm https://raw.githubusercontent.com/kill136/claude-code-open/private_web_ui/install.ps1 | iex
• macOS: curl -fsSL https://raw.githubusercontent.com/kill136/claude-code-open/private_web_ui/install.sh | bash
• Linux: curl -fsSL https://raw.githubusercontent.com/kill136/claude-code-open/private_web_ui/install.sh | bash

在线体验：http://voicegpt.site:3456/"""

Tool.objects.get_or_create(
    name='免费开源Web IDE',
    defaults={
        'slug': slugify('免费开源Web IDE', allow_unicode=True),
        'short_description': '免费开源的Web IDE，支持使用Opus 4.6',
        'full_description': full_desc,
        'website_url': 'https://www.chatbi.site/',
        'category': free_cat,
        'is_published': True,
        'is_featured': True
    }
)

print('✓ 添加免费开源Web IDE工具')
