#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 获取或创建分类
marketing_cat, _ = Category.objects.get_or_create(
    name='营销推广',
    defaults={
        'slug': slugify('营销推广', allow_unicode=True),
        'description': 'SEO、内容营销、品牌推广等营销工具和方法'
    }
)

# 添加 GEO 指南
full_desc = """GEO（生成式引擎优化）实战指南

**什么是 GEO？**
当用户借助 AI 提问时，AI 会将你输出的内容或观点直接当做答案的一部分；或者在生成答案时，引用你在其他平台上发布的内容链接。

**普通人做好 GEO 的 3 个关键点：**

1. **分析客户提问方式**
   - 研究你的目标客户会用什么样的语句向 AI 提问
   - 了解他们的痛点和需求表达方式

2. **持续内容创作**
   - 基于客户可能的提问进行针对性内容创作
   - 发布在百家号、今日头条、知乎等平台
   - 需要坚持长期写作，积累内容资产

3. **明确个人/品牌定位**
   - 给自己或公司找到一个清晰的定位
   - 例如："教培精细管理专家刘一一"
   - 所有发布的内容都围绕这个定位，持续巩固

做到这 3 点，基本上就能做好 GEO 优化。"""

Tool.objects.get_or_create(
    name='GEO生成式引擎优化指南',
    defaults={
        'slug': slugify('GEO生成式引擎优化指南', allow_unicode=True),
        'short_description': '让AI主动推荐你的内容：GEO优化3步法',
        'full_description': full_desc,
        'website_url': 'https://ai-tool.indevs.in/',
        'category': marketing_cat,
        'is_published': True,
        'is_featured': True
    }
)

print('✓ 添加 GEO 生成式引擎优化指南')
