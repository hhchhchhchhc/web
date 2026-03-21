#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category = Category.objects.get(name='免费用最高级大模型')

Tool.objects.update_or_create(
    name='NPC-API公益站',
    defaults={
        'slug': slugify('NPC-API公益站', allow_unicode=True),
        'short_description': '免费DeepSeek模型API，25亿token额度',
        'full_description': '''NPC-API公益站点

访问地址：https://npcodex.kiroxubei.tech

特点：
- 支持DeepSeek模型
- 总共25亿token额度
- OpenAI接口聚合管理
- 注册开放

使用说明：
注册账号后即可获取API密钥，支持OpenAI标准接口调用

来源：https://linux.do/t/topic/337620''',
        'website_url': 'https://npcodex.kiroxubei.tech',
        'category': category,
        'is_published': True,
        'is_featured': True
    }
)

print("✅ NPC-API工具添加成功！")
