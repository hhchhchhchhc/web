#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 获取创业资源分类
category, _ = Category.objects.get_or_create(
    name='创业资源',
    defaults={'slug': slugify('创业资源', allow_unicode=True)}
)

# 添加 Linux.do
Tool.objects.get_or_create(
    name='Linux.do',
    defaults={
        'slug': 'linux-do',
        'short_description': '中文Linux技术社区，开发者交流和学习平台',
        'full_description': '''🐧 Linux.do - 优质中文Linux社区

🎯 核心价值：
• 活跃的中文Linux技术社区
• 高质量的技术讨论和分享
• 开发者经验交流平台
• 友好的新手学习环境

✨ 主要内容：
• Linux系统使用和配置
• 服务器运维经验分享
• 开源软件讨论
• 技术问题互助

🎯 适用人群：
• Linux学习者和爱好者
• 服务器运维工程师
• 开源技术爱好者
• 独立开发者''',
        'website_url': 'https://linux.do',
        'category': category,
        'is_published': True,
        'is_featured': True
    }
)

print("✅ Linux.do 添加成功！")
