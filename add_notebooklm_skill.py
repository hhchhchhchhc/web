#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category = Category.objects.get(name='AI办公工具')

Tool.objects.update_or_create(
    name='Anything to NotebookLM',
    defaults={
        'slug': slugify('Anything to NotebookLM', allow_unicode=True),
        'short_description': '多源内容智能处理器：支持微信公众号、网页、YouTube、PDF、Markdown等，自动上传到NotebookLM并生成播客/PPT/思维导图等多种格式',
        'full_description': '''多源内容 → NotebookLM 智能处理器

GitHub: https://github.com/joeseesun/anything-to-notebooklm

支持内容源（15+种格式）：
- 微信公众号（绕过反爬虫）
- YouTube视频（自动提取字幕）
- 任意网页、PDF、EPUB电子书
- Word/PowerPoint/Excel文档
- 图片（OCR）、音频（转录）
- CSV/JSON/XML等结构化数据

可生成格式：
🎙️ 播客 - 通勤路上听（2-5分钟）
📊 PPT - 团队分享（1-3分钟）
🗺️ 思维导图 - 理清结构（1-2分钟）
📝 Quiz - 自测掌握（1-2分钟）
🎬 视频、📄 报告、📈 信息图、📋 闪卡

使用方式：
这是一个Claude Code Skill，需要安装到~/.claude/skills/目录
完全自然语言交互，无需记命令

技术特点：
- 智能识别内容源类型
- 全自动处理流程
- 支持多源整合
- 本地优先处理敏感内容''',
        'website_url': 'https://github.com/joeseesun/anything-to-notebooklm',
        'category': category,
        'is_published': True,
        'is_featured': True
    }
)

print("✅ Anything to NotebookLM工具添加成功！")
