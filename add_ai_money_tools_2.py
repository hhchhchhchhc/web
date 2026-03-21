#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

tools_data = [
    {
        'name': 'Kling可灵',
        'short_description': '图转视频AI工具，支持人物参考生成视频，保证人物一致性',
        'full_description': 'Kling (可灵) 是强大的图转视频AI工具，支持人物参考生成视频，能够保证人物唯一性和一致性。适合制作AI短剧、漫剧等视频内容。',
        'website_url': 'https://klingai.com/',
        'category_name': 'AI视频工具'
    },
    {
        'name': 'Vidu',
        'short_description': '图转视频AI工具，支持人物参考生成高质量视频',
        'full_description': 'Vidu是国产图转视频AI工具，支持人物参考生成视频，保证人物一致性。适合内容创作者制作短视频和AI漫剧。',
        'website_url': 'https://www.vidu.studio/',
        'category_name': 'AI视频工具'
    },
    {
        'name': 'Suno',
        'short_description': 'AI音乐生成工具，可创作高品质原创歌曲',
        'full_description': 'Suno是领先的AI音乐生成工具，能够根据文字描述生成高品质的原创音乐和歌曲。支持多种音乐风格，适合视频配乐和音乐创作。',
        'website_url': 'https://suno.ai/',
        'category_name': 'AI音频工具'
    },
    {
        'name': 'MiniMax海螺AI',
        'short_description': 'AI音乐生成工具，支持生成长达4分钟的完整歌曲',
        'full_description': 'MiniMax海螺AI 1.5支持生成长达4分钟的完整歌曲，具备清晰的歌曲结构和高音质输出。适合音乐创作和视频配乐。',
        'website_url': 'https://hailuoai.com/',
        'category_name': 'AI音频工具'
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

print('\n第二批完成！')
