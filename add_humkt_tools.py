#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 1. Google账号服务
account_category, _ = Category.objects.get_or_create(
    name='账号服务',
    defaults={'slug': slugify('账号服务', allow_unicode=True)}
)

Tool.objects.get_or_create(
    name='超低价谷歌账号',
    defaults={
        'slug': slugify('超低价谷歌账号', allow_unicode=True),
        'short_description': '四元多超低价购买谷歌账号，性价比极高',
        'full_description': '''🎯 超低价谷歌账号购买服务

💰 价格优势：
• 仅需四元多即可购买谷歌账号
• 市场最低价，性价比超高
• 适合批量购买和测试使用

✅ 服务特点：
• 快速交付，即买即用
• 账号稳定可靠
• 支持多种用途

🛒 购买渠道：
访问 humkt.com 了解详情并购买''',
        'website_url': 'https://www.humkt.com',
        'category': account_category,
        'is_published': True,
        'is_featured': True
    }
)

# 2. NotebookLM
ai_category, _ = Category.objects.get_or_create(
    name='AI办公工具',
    defaults={'slug': slugify('AI办公工具', allow_unicode=True)}
)

Tool.objects.get_or_create(
    name='NotebookLM',
    defaults={
        'slug': slugify('NotebookLM', allow_unicode=True),
        'short_description': 'Google推出的AI笔记和研究助手，帮你整理和分析文档',
        'full_description': '''🤖 NotebookLM - Google AI笔记助手

NotebookLM是Google推出的AI驱动的笔记和研究工具，能够帮助你更好地理解和组织信息。

✨ 核心功能：
• 智能文档分析：上传PDF、文本等文档，AI自动提取关键信息
• 自动生成摘要：快速理解长文档的核心内容
• 智能问答：基于你的文档内容回答问题
• 知识整合：将多个来源的信息整合在一起

🎯 适用场景：
• 学术研究和论文写作
• 工作文档整理和分析
• 学习笔记管理
• 项目资料汇总

💡 使用方式：
完全免费，使用Google账号即可登录使用''',
        'website_url': 'https://notebooklm.google.com',
        'category': ai_category,
        'is_published': True,
        'is_featured': True
    }
)

print("✅ 工具添加成功！")
print("- 超低价谷歌账号 (账号服务)")
print("- NotebookLM (AI办公工具)")
