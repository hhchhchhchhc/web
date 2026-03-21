#!/usr/bin/env python
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category, _ = Category.objects.get_or_create(
    name='免费资源',
    defaults={'slug': slugify('免费资源', allow_unicode=True)}
)

Tool.objects.get_or_create(
    name='上海交大张伟楠强化学习课程字幕',
    defaults={
        'slug': 'sjtu-rl-course-subtitles',
        'short_description': '上海交通大学张伟楠教授强化学习课程完整字幕，免费下载学习顶尖AI课程资源',
        'full_description': '上海交通大学张伟楠教授的强化学习课程字幕资源，帮助你更好地理解和学习强化学习的核心概念。\n\n百度网盘链接：https://pan.baidu.com/s/1_THLnl2gq4MtAW77rFnRxw?pwd=hdbf\n提取码：hdbf\n\n适合AI学习者、研究生和对强化学习感兴趣的开发者。',
        'website_url': 'https://pan.baidu.com/s/1_THLnl2gq4MtAW77rFnRxw?pwd=hdbf',
        'category': category,
        'is_published': True,
        'is_featured': False
    }
)

print("✅ 已添加工具：上海交大张伟楠强化学习课程字幕")
