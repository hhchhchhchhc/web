#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 获取创业资源分类
startup_category, _ = Category.objects.get_or_create(
    name='创业资源',
    defaults={'slug': slugify('创业资源', allow_unicode=True)}
)

# 5. GitHub
Tool.objects.get_or_create(
    name='GitHub',
    defaults={
        'slug': 'github',
        'short_description': '全球最大代码托管平台，分析开源项目和技术趋势',
        'full_description': '''💻 GitHub - 开发者必备平台

🎯 核心价值：
• 分析优秀开源项目的代码实现
• 学习顶级开发者的编程技巧
• 发现热门技术趋势和工具
• 展示个人技术能力

✨ 主要功能：
• 代码托管和版本控制
• 开源项目浏览和学习
• 技术趋势榜单（Trending）
• 开发者协作和交流

🎯 适用场景：
• 学习优秀代码实现
• 寻找开源工具和库
• 了解技术发展趋势
• 构建个人技术品牌''',
        'website_url': 'https://github.com',
        'category': startup_category,
        'is_published': True,
        'is_featured': True
    }
)

# 6. Reddit
Tool.objects.get_or_create(
    name='Reddit',
    defaults={
        'slug': 'reddit',
        'short_description': '全球最大社区平台，学习社区增长和用户运营',
        'full_description': '''🌐 Reddit - 社区增长案例库

🎯 核心价值：
• 学习成功产品的社区增长策略
• 了解用户真实反馈和需求
• 发现细分领域的机会
• 产品发布和获取早期用户

✨ 主要功能：
• 数万个垂直细分社区
• 真实用户讨论和反馈
• AMA（Ask Me Anything）访谈
• 产品发布和推广渠道

🎯  适用场景：
• 研究目标用户需求
• 学习社区运营方法
• 产品发布和推广
• 寻找创业灵感''',
        'website_url': 'https://www.reddit.com',
        'category': startup_category,
        'is_published': True,
        'is_featured': True
    }
)

print("✅ 最后一批工具添加成功！")
print("\n所有信息源工具已添加完成：")
print("- Indie Hackers")
print("- Product Hunt")
print("- V2EX酷工作")
print("- Polymarket")
print("- GitHub")
print("- Reddit")
