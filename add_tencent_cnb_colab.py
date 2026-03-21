#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

tools_data = [
    {
        'name': '腾讯云原生开发CNB',
        'short_description': '免费云原生开发环境，提供GPU算力，每月1600核时',
        'full_description': '腾讯云原生开发CNB提供免费的云原生开发环境，配备GPU算力资源，每月提供1600核时的免费额度。支持容器化开发，适合云原生应用开发和AI模型训练。',
        'website_url': 'https://cnb.cloud.tencent.com/',
        'category_name': '云算力平台'
    },
    {
        'name': 'Colab Pro学生优惠',
        'short_description': '闲鱼401元购买一年Colab Pro学生包，超值优惠',
        'full_description': '通过闲鱼平台可以401元购买Google Colab Pro学生包一年使用权，相比官方价格更优惠。Colab Pro提供更长的运行时间、更好的GPU资源和更大的内存。',
        'website_url': 'https://www.xianyu.com/',
        'category_name': '🎁 限时福利'
    }
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

print('\n完成！')
