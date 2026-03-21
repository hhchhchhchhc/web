#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 创建创业资源分类
startup_category, _ = Category.objects.get_or_create(
    name='创业资源',
    defaults={'slug': slugify('创业资源', allow_unicode=True)}
)

# 1. Indie Hackers
Tool.objects.get_or_create(
    name='Indie Hackers',
    defaults={
        'slug': 'indie-hackers',
        'short_description': '独立开发者社区，查看真实营收数据和创业案例',
        'full_description': '''🚀 Indie Hackers - 独立开发者必备社区

💰 核心价值：
• 真实营收数据展示，透明的创业案例
• 独立开发者分享产品从0到1的完整过程
• 学习如何将想法变现为实际收入

✨ 主要功能：
• 浏览数千个独立项目的营收报告
• 创始人访谈和经验分享
• 活跃的开发者社区讨论
• 产品发布和反馈

🎯 适用人群：
• 独立开发者和创业者
• 想了解产品变现路径的人
• 寻找创业灵感和案例的人''',
        'website_url': 'https://www.indiehackers.com',
        'category': startup_category,
        'is_published': True,
        'is_featured': True
    }
)

# 2. Product Hunt
Tool.objects.get_or_create(
    name='Product Hunt',
    defaults={
        'slug': 'product-hunt',
        'short_description': '全球最大的产品发现平台，追踪早期创新项目',
        'full_description': '''🔍 Product Hunt - 产品发现第一站

🎯 核心价值：
• 每天发现最新最酷的产品和工具
• 追踪早期项目，抓住趋势机会
• 产品发布和获取早期用户的最佳平台

✨ 主要功能：
• 每日精选优质新产品
• 产品投票和评论系统
• 创始人分享产品故事
• Maker社区交流

🎯 适用场景：
• 产品发布和推广
• 寻找创业灵感
• 了解行业趋势
• 获取早期用户反馈''',
        'website_url': 'https://www.producthunt.com',
        'category': startup_category,
        'is_published': True,
        'is_featured': True
    }
)

print("✅ 第一批工具添加成功！")
