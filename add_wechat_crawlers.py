#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 获取爬虫分类
category = Category.objects.get(name='爬虫')

# 工具数据
tools_data = [
    {
        'name': 'Wechat Article Exporter',
        'short_description': '开源的微信公众号文章导出工具，支持批量下载和格式转换',
        'full_description': 'Wechat Article Exporter是一个开源的微信公众号文章导出工具，支持批量下载公众号文章，并可以导出为多种格式。功能强大，使用简单。',
        'website_url': 'https://github.com/wechat-article/wechat-article-exporter',
    },
    {
        'name': 'MPText公众号下载器',
        'short_description': '在线微信公众号文章下载工具，无需安装即可使用',
        'full_description': 'MPText是一个在线的微信公众号文章下载工具，支持快速下载公众号文章，无需安装任何软件，直接在浏览器中使用即可。',
        'website_url': 'https://down.mptext.top/',
    },
    {
        'name': '微信公众号爬虫教程',
        'short_description': 'B站视频教程，教你如何爬取微信公众号文章',
        'full_description': '这是一个详细的B站视频教程，手把手教你如何使用Python爬取微信公众号文章，适合初学者学习。',
        'website_url': 'https://www.bilibili.com/video/BV1BN41157y9/',
    }
]

# 添加工具
for tool_data in tools_data:
    tool, created = Tool.objects.get_or_create(
        name=tool_data['name'],
        defaults={
            **tool_data,
            'category': category
        }
    )

    if created:
        print(f'✓ 已添加: {tool.name}')
    else:
        print(f'- 已存在: {tool.name}')

print('\n完成！')
