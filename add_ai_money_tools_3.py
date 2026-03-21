#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

tools_data = [
    {
        'name': 'CodeFlying',
        'short_description': '通过中文指令直接生成可部署的微信小程序、App或网页应用',
        'full_description': 'CodeFlying支持通过中文指令直接生成可部署的微信小程序、App或网页应用，无需编写代码。适合非技术人员快速开发应用程序。',
        'website_url': 'https://codeflying.com/',
        'category_name': 'AI开发平台'
    },
    {
        'name': 'ShellAgent 2.0',
        'short_description': '无代码开发平台，支持中文指令生成小程序和应用',
        'full_description': 'ShellAgent 2.0支持通过中文指令直接生成可部署的微信小程序、App或网页应用，无需编写代码。降低开发门槛，提升开发效率。',
        'website_url': 'https://shellagent.ai/',
        'category_name': 'AI开发平台'
    },
    {
        'name': 'AutoGLM 2.0',
        'short_description': '跨硬件AI助手，可替用户操作手机和电脑执行复杂指令',
        'full_description': 'AutoGLM 2.0可跨硬件替用户操作手机和电脑上的常用App执行复杂指令，实现自动化操作。适合提升工作效率和自动化日常任务。',
        'website_url': 'https://chatglm.cn/',
        'category_name': 'AI办公工具'
    },
    {
        'name': 'AI赚钱信息差完整指南',
        'short_description': 'AI工具变现方法、热门案例和实操技巧全面总结',
        'full_description': '涵盖AI图像生成、视频制作、音频创作等工具的赚钱方法。包括虚拟资料售卖、情绪价值产品、AI二创漫剧、实物变现等多种变现模式。提供精细化制作建议、提示词工程技巧和垂直赛道选择策略。',
        'website_url': 'http://ai-tool.indevs.in/',
        'category_name': '赚钱技巧'
    },
]

for tool_data in tools_data:
    category_name = tool_data.pop('category_name')
    category = Category.objects.get(name=category_name)

    tool, created = Tool.objects.get_or_create(
        name=tool_data['name'],
        defaults={
            **tool_data,
            'category': category
        }
    )

    if created:
        print(f'✓ 已添加: {tool.name} → {category.name}')
    else:
        print(f'- 已存在: {tool.name}')

print('\n第三批完成！')
