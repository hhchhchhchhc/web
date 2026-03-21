#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 精选工具列表
CURATED_TOOLS = [
    {
        'category': '网络工具',
        'tools': [
            {'name': '闪电云加速', 'url': 'https://shandianpro.com/#/dashboard', 'desc': 'Clash Core 网络加速工具'},
        ]
    },
    {
        'category': '信息管理',
        'tools': [
            {'name': 'FOLLOW', 'url': 'https://follow.is/', 'desc': '超强RSS信息管理工具'},
        ]
    },
    {
        'category': '云算力平台',
        'tools': [
            {'name': 'DigitalOcean', 'url': 'https://www.digitalocean.com/', 'desc': '每个账户可获得200美金免费额度'},
            {'name': '奇绩算力', 'url': 'https://www.miracleplus.com/', 'desc': '为加速科研创业提供免费高性能算力'},
            {'name': '潞晨云', 'url': 'https://www.luchencloud.com/', 'desc': '高性价比GPU算力租赁，4090 1元/h，A100 80G 5.99/h'},
        ]
    },
    {
        'category': 'AI工具',
        'tools': [
            {'name': 'Linux.do论坛', 'url': 'https://linux.do/', 'desc': 'AI效率工具讨论社区'},
            {'name': 'Claude Max租用平台', 'url': 'https://www.claudemax.com/', 'desc': '大模型超低价租用，GPT 20元/月，Claude Max 88元/月'},
            {'name': 'Markmap思维导图', 'url': 'https://www.min87.com/tools/markmap/index_zh.html', 'desc': 'AI思维导图工具'},
            {'name': '通义千问', 'url': 'https://tongyi.aliyun.com/', 'desc': '视频和播客总结工具'},
            {'name': '豆包浏览器插件', 'url': 'https://www.doubao.com/', 'desc': '多网页总结AI助手'},
            {'name': 'Kimi插件', 'url': 'https://kimi.moonshot.cn/', 'desc': '总结当前界面内容'},
        ]
    },
    {
        'category': '视频工具',
        'tools': [
            {'name': 'Video Speed Controller', 'url': 'https://chrome.google.com/webstore', 'desc': '视频倍速播放插件，支持0.07-16倍速'},
            {'name': 'YouTube字幕提取', 'url': 'https://www.youtube.com/', 'desc': '获取YouTube视频文稿工具'},
        ]
    },
    {
        'category': '搜索工具',
        'tools': [
            {'name': 'SearchEngineJump', 'url': 'https://greasyfork.org/', 'desc': '搜索引擎快捷跳转油猴脚本'},
            {'name': '凌风云', 'url': 'https://www.lingfengyun.com/', 'desc': '免费搜索研报合集'},
            {'name': '微信公众号爬虫插件', 'url': 'https://www.chajianxw.com/product-tool/19726.html', 'desc': '获取公众号所有文章URL'},
        ]
    },
]

print('导入精选工具...\n')

imported = 0
for cat_data in CURATED_TOOLS:
    cat_name = cat_data['category']
    cat, _ = Category.objects.get_or_create(
        name=cat_name,
        defaults={'slug': slugify(cat_name, allow_unicode=True)}
    )

    for tool_data in cat_data['tools']:
        slug = slugify(tool_data['name'], allow_unicode=True) or f"tool-{imported}"
        counter = 1
        while Tool.objects.filter(slug=slug).exists():
            slug = f"{slugify(tool_data['name'], allow_unicode=True)}-{counter}"
            counter += 1

        Tool.objects.create(
            name=tool_data['name'],
            slug=slug,
            short_description=tool_data['desc'],
            full_description=tool_data['desc'],
            website_url=tool_data['url'],
            category=cat,
            is_published=True
        )
        imported += 1

print(f'✓ 导入精选工具: {imported} 个')
