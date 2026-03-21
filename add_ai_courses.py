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
        'name': 'AI大模型全栈工程师第9期',
        'slug': 'ai-fullstack-engineer-phase9',
        'short_description': 'AI大模型全栈工程师第9期完整课程，质量优秀，适合系统学习AI大模型开发',
        'full_description': 'AI大模型全栈工程师第9期完整课程资源，课程质量优秀，讲解清晰舒适。\n\n夸克网盘链接：https://pan.quark.cn/s/1bdd751364ff\n\n适合想要系统学习AI大模型全栈开发的工程师和开发者。',
        'url': 'https://pan.quark.cn/s/1bdd751364ff'
    },
    {
        'name': '聚客大模型开发工程师VIP系统课第五期',
        'slug': 'juke-llm-engineer-vip-phase5',
        'short_description': '聚客大模型开发工程师VIP系统课程第五期（L0、L1、L2完整课程）',
        'full_description': '聚客大模型开发工程师VIP系统课程第五期，包含L0、L1、L2完整课程内容。\n\n夸克网盘链接：https://pan.quark.cn/s/57acdc9059a5\n\n系统化学习大模型开发的完整课程体系。',
        'url': 'https://pan.quark.cn/s/57acdc9059a5'
    },
    {
        'name': '慕课网LLM大语言模型算法特训',
        'slug': 'imooc-llm-algorithm-training',
        'short_description': '慕课网体系课-LLM大语言模型算法特训，助你转型AI大语言模型算法工程师',
        'full_description': '慕课网体系课程：LLM大语言模型算法特训，帮助你系统学习并转型成为AI大语言模型算法工程师。\n\n夸克网盘链接：https://pan.quark.cn/s/07c9f8ed2c9b\n\n适合想要深入学习LLM算法的开发者。',
        'url': 'https://pan.quark.cn/s/07c9f8ed2c9b'
    },
    {
        'name': '图灵学院2025年AI大模型全栈工程师2.0',
        'slug': 'turing-ai-fullstack-2025-v2',
        'short_description': '图灵学院2025年全新AI大模型全栈工程师课程2.0版本',
        'full_description': '图灵学院2025年全"薪"AI大模型全栈工程师课程【2.0】，最新版本课程内容。\n\n夸克网盘链接：https://pan.quark.cn/s/a57fbd4b7099\n\n2025年最新AI大模型全栈开发课程。',
        'url': 'https://pan.quark.cn/s/a57fbd4b7099'
    },
    {
        'name': '人工智能顶级实战工程师就业课程',
        'slug': 'ai-top-engineer-employment-course',
        'short_description': '人工智能顶级实战工程师就业课程，面向就业的AI实战培训',
        'full_description': '人工智能顶级实战工程师就业课程，专注于实战技能培养，帮助学员顺利就业。\n\n夸克网盘链接：https://pan.quark.cn/s/dfdf84400cb9\n\n适合准备进入AI行业就业的学习者。',
        'url': 'https://pan.quark.cn/s/dfdf84400cb9'
    },
    {
        'name': '大模型面试资料',
        'slug': 'llm-interview-materials',
        'short_description': '大模型面试资料合集，助力AI大模型岗位面试准备',
        'full_description': '大模型面试资料完整合集，涵盖AI大模型相关岗位的面试准备资料。\n\n夸克网盘链接：https://pan.quark.cn/s/908040c2e4d1\n\n适合准备大模型相关岗位面试的求职者。',
        'url': 'https://pan.quark.cn/s/908040c2e4d1'
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

print("\n🎉 所有AI课程资源已成功添加！")
