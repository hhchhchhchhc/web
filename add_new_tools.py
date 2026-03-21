#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 工具数据
tools_data = [
    {
        'name': 'Gemini Deep Research',
        'short_description': 'Google推出的深度研究工具，能够进行全面的信息搜索和分析',
        'full_description': 'Gemini Deep Research是Google推出的AI深度研究工具，能够自动搜索、分析和综合大量信息，为用户提供全面深入的研究报告。适合学术研究、市场调研等场景。',
        'website_url': 'https://deepresearch.google.com/',
        'category_name': 'AI搜索引擎'
    },
    {
        'name': 'Anygen',
        'short_description': '字节跳动推出的批量调研工具，支持大规模问卷调查和数据分析',
        'full_description': 'Anygen是字节跳动推出的AI批量调研工具，能够快速生成调研问卷、批量收集数据并进行智能分析，大幅提升调研效率。适合市场调研、用户研究等场景。',
        'website_url': 'https://www.anygen.cn/',
        'category_name': 'AI办公工具'
    },
    {
        'name': 'GPUShare',
        'short_description': '低价GPU云算力租赁平台，提供性价比高的GPU资源',
        'full_description': 'GPUShare是一个GPU云算力租赁平台，提供低价高性能的GPU资源，支持深度学习训练、AI推理等场景。按需付费，灵活便捷。',
        'website_url': 'https://www.gpushare.com/',
        'category_name': '云算力平台'
    },
    {
        'name': 'AutoDL',
        'short_description': '低价GPU云算力平台，专注深度学习训练和推理',
        'full_description': 'AutoDL是国内领先的GPU云算力平台，提供低价高性能的GPU资源，支持PyTorch、TensorFlow等主流深度学习框架。提供Jupyter、SSH等多种访问方式。',
        'website_url': 'https://www.autodl.com/',
        'category_name': '云算力平台'
    }
]

# 添加工具
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
