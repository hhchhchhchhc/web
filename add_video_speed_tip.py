#!/usr/bin/env python
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category, _ = Category.objects.get_or_create(
    name='视频工具',
    defaults={'slug': slugify('视频工具', allow_unicode=True)}
)

Tool.objects.get_or_create(
    name='AI加速看视频方法',
    defaults={
        'slug': 'ai-video-speed-watching',
        'short_description': '使用千问或飞书妙记3~16倍速看视频，配合字幕高效学习',
        'full_description': '快速看视频的高效方法：\n\n1. 下载视频\n2. 上传到千问或飞书妙记\n3. 使用3~16倍速播放\n4. 配合字幕观看\n\n如果是5倍速，可以使用浏览器加速插件辅助。这个方法特别适合学习课程视频、会议录像等需要快速获取信息的场景。',
        'website_url': 'https://tongyi.aliyun.com/',
        'category': category,
        'is_published': True,
        'is_featured': False
    }
)

print("✅ 已添加工具：AI加速看视频方法")
