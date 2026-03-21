#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

tools_data = [
    {
        'name': '凌风云网盘搜索',
        'short_description': '强大的网盘资源搜索引擎，可搜索各类电子书和文档',
        'full_description': '凌风云是一个专业的网盘资源搜索引擎，支持搜索百度网盘、阿里云盘等多个网盘平台的资源，特别适合查找电子书、文档、学习资料等内容。',
        'website_url': 'https://www.lingfengyun.com/',
        'category_name': '搜索工具'
    },
    {
        'name': 'Z-Library',
        'short_description': '世界上最大的电子图书馆，免费访问海量电子书',
        'full_description': 'Z-Library是全球最大的免费电子图书馆，收录了数百万本电子书和学术论文，支持多种格式下载。提供中文界面，方便查找各类图书资源。',
        'website_url': 'https://zh.z-lib.gl/',
        'category_name': '搜索工具'
    },
    {
        'name': '鸠摩搜书',
        'short_description': '专业的电子书搜索引擎，聚合多个电子书源',
        'full_description': '鸠摩搜书是一个聚合型电子书搜索引擎，整合了多个电子书资源站点，提供便捷的一站式搜索服务，支持多种格式的电子书下载。',
        'website_url': 'https://www.jiumodiary.com/',
        'category_name': '搜索工具'
    },
    {
        'name': 'Library Genesis',
        'short_description': '学术资源搜索引擎，提供海量学术论文和电子书',
        'full_description': 'Library Genesis (LibGen) 是一个专注于学术资源的搜索引擎，收录了大量学术论文、教材、专业书籍等，是科研人员和学生的重要资源库。',
        'website_url': 'https://libgen.is/',
        'category_name': '搜索工具'
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
