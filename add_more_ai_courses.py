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

courses = [
    {
        'name': '路飞AI大模型就业班',
        'slug': 'luffy-ai-llm-employment-class',
        'short_description': '路飞AI大模型就业班完整课程，专注AI大模型就业培训',
        'full_description': '路飞AI大模型就业班完整课程资源，专注于AI大模型领域的就业培训。\n\n夸克网盘链接：https://pan.quark.cn/s/589926d203b5\n\n适合想要进入AI大模型行业就业的学习者。',
        'url': 'https://pan.quark.cn/s/589926d203b5'
    },
    {
        'name': '丁师兄大模型训练营',
        'slug': 'ding-shixiong-llm-bootcamp',
        'short_description': '丁师兄大模型训练营完整课程，系统学习大模型开发',
        'full_description': '丁师兄大模型训练营完整课程资源，系统化学习大模型开发技术。\n\n夸克网盘链接：https://pan.quark.cn/s/2bd637994285\n\n适合想要系统学习大模型开发的工程师。',
        'url': 'https://pan.quark.cn/s/2bd637994285'
    }
]

for course in courses:
    Tool.objects.get_or_create(
        name=course['name'],
        defaults={
            'slug': course['slug'],
            'short_description': course['short_description'],
            'full_description': course['full_description'],
            'website_url': course['url'],
            'category': category,
            'is_published': True,
            'is_featured': False
        }
    )
    print(f"✅ 已添加工具：{course['name']}")

print("\n🎉 AI课程资源添加完成！")
