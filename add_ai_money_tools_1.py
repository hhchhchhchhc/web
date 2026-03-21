#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# Create 赚钱技巧 category
category, created = Category.objects.get_or_create(
    name='赚钱技巧',
    defaults={'description': 'AI赚钱方法、变现案例和实操技巧'}
)

if created:
    print(f'✓ 已创建分类: {category.name}')
else:
    print(f'- 分类已存在: {category.name}')

# Tools data
tools_data = [
    # AI图像工具
    {
        'name': 'Nano Banana Pro',
        'short_description': '顶级AI生图模型，擅长人物一致性、漫画绘画及手办风格生成',
        'full_description': 'Nano Banana Pro (Lovart/Gemini) 是目前顶级的AI图像生成模型，在人物一致性、漫画绘画及手办风格生成方面表现卓越。适合创作者制作高质量的角色设计和商业插画。',
        'website_url': 'https://lovart.ai/',
        'category_name': 'AI图像工具'
    },
    {
        'name': 'Seedance 2.0',
        'short_description': '即梦AI，支持全能参考功能，可通过图片、音频、视频控制生成视频',
        'full_description': 'Seedance 2.0 (即梦) 支持"全能参考"功能，可通过图片、音频、视频控制生成视频，解决运镜、剪辑及人物一致性问题，特别适合制作高质量短剧和AI漫剧。',
        'website_url': 'https://jimeng.jianying.com/',
        'category_name': 'AI视频工具'
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

print('\n第一批完成！')
