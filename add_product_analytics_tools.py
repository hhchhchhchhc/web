#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category, _ = Category.objects.get_or_create(
    name='营销推广',
    defaults={'slug': slugify('营销推广', allow_unicode=True)}
)

tools_data = [
    {
        'name': 'Plausible Analytics',
        'short_description': '轻量、注重隐私的产品分析工具，小排老师推荐',
        'full_description': '''2/ 产品分析工具推荐

小排老师推荐：Plausible 和 Clarity。
如果你之前一直使用谷歌分析（Google Analytics），可以把这两个作为关键补充方案。
这个产品分析方法很有启发，尤其适合做行为洞察和转化优化。''',
        'website_url': 'https://plausible.io/',
        'is_featured': True,
    },
    {
        'name': 'Microsoft Clarity',
        'short_description': '免费用户行为分析工具，含热图与会话回放，小排老师推荐',
        'full_description': '''2/ 产品分析工具推荐

小排老师推荐：Plausible 和 Clarity。
如果你之前一直使用谷歌分析（Google Analytics），可以把这两个作为关键补充方案。
这个产品分析方法很有启发，尤其适合做行为洞察和转化优化。''',
        'website_url': 'https://clarity.microsoft.com/',
        'is_featured': True,
    },
]

for item in tools_data:
    tool, created = Tool.objects.update_or_create(
        name=item['name'],
        defaults={
            'slug': slugify(item['name'], allow_unicode=True),
            'short_description': item['short_description'],
            'full_description': item['full_description'],
            'website_url': item['website_url'],
            'category': category,
            'is_published': True,
            'is_featured': item['is_featured'],
        }
    )
    print(f"{'✅ 已新增' if created else '✅ 已更新'}: {tool.name} -> {tool.category.name}")
