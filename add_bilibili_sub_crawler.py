#!/usr/bin/env python3
import os

import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool


category = Category.objects.get(name='爬虫')

tool, created = Tool.objects.update_or_create(
    name='B站 UP 主字幕批量爬取工具',
    defaults={
        'slug': slugify('B站 UP 主字幕批量爬取工具', allow_unicode=True),
        'short_description': '输入 UP 主 UID，自动爬取该 UP 主全部视频的全部字幕',
        'full_description': (
            '开源的 B 站字幕批量爬取工具。输入 UP 主 UID 后，可以自动遍历该 UP 主的全部视频，'
            '并抓取每个视频的全部字幕内容，适合做内容分析、语料整理、视频研究和批量转存。'
        ),
        'website_url': 'https://github.com/hanchihuang/bilibili_sub_crawler',
        'category': category,
        'is_published': True,
        'is_featured': False,
    }
)

print(f"{'✓ 已新增' if created else '✓ 已更新'}: {tool.name} -> {tool.category.name}")
