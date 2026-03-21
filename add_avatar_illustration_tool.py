#!/usr/bin/env python
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# Get or create category
category, _ = Category.objects.get_or_create(
    name='赚钱技巧',
    defaults={'slug': slugify('赚钱技巧', allow_unicode=True)}
)

# Add tool
Tool.objects.get_or_create(
    name='𝙎𝙝𝙖𝙧𝙚头像｜一见钟情的插画头像',
    defaults={
        'slug': slugify('share-avatar-illustration', allow_unicode=False),
        'short_description': '涨粉秘籍：使用精美插画头像提升账号吸引力，一见钟情的视觉设计让你的粉丝量快速增长',
        'full_description': '在社交媒体运营中，头像是用户对你的第一印象。使用Pixabay提供的高质量免费插画作为头像，可以显著提升账号的专业度和吸引力。\n\n推荐搜索关键词：\n• 治愈系插画\n• 温柔风格\n• 小清新设计\n\n这些风格的插画头像特别适合个人品牌建设，能够快速建立信任感，是涨粉的有效秘籍之一。',
        'website_url': 'https://pixabay.com/zh/illustrations/',
        'category': category,
        'is_published': True,
        'is_featured': False
    }
)

print("✅ 已添加工具：𝙎𝙝𝙖𝙧𝙚头像｜一见钟情的插画头像")
