#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category = Category.objects.get(name='免费用最高级大模型')

Tool.objects.update_or_create(
    name='无限Codex API',
    defaults={
        'slug': slugify('无限Codex API', allow_unicode=True),
        'short_description': '免费无限RPM的Codex API访问，每日自动激活',
        'full_description': '''免费无限Codex API分发系统

访问地址：https://codex.mqc.me

特点：
- RPM无限制
- 每日北京时间早上8:00自动激活所有密钥
- 连续5小时无使用会自动停用，重新登录即可激活

使用说明：
访问登录页面获取API密钥，支持各种AI开发需求

来源：https://linux.do/t/topic/343089''',
        'website_url': 'https://codex.mqc.me',
        'category': category,
        'is_published': True,
        'is_featured': True
    }
)

print("✅ Codex API工具添加成功！")
