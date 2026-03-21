import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 获取网盘资源分类
category, _ = Category.objects.get_or_create(
    name='网盘资源',
    defaults={'description': '优质网盘资源和资料分享', 'order': 16}
)

# 添加私募路演
tool, created = Tool.objects.get_or_create(
    name='私募路演',
    defaults={
        'short_description': '私募基金路演资料合集，深入了解私募行业运作和投资策略',
        'full_description': '''私募路演资源包：

【资源内容】
专业的私募基金路演资料合集，涵盖私募基金的运作模式、投资策略、行业分析等核心内容。

【适合人群】
• 私募基金从业者
• 投资机构研究员
• 金融行业学习者
• 资产管理从业者
• 投资者教育需求者

【资源价值】
深入了解私募基金行业的运作机制、投资理念、风险控制等专业知识，帮助提升金融投资专业能力。

百度网盘提取码: t4fm''',
        'website_url': 'https://pan.baidu.com/s/1CEjSpkKJNXiSxHuBXzdCsA?pwd=t4fm',
        'category': category,
        'is_published': True,
    }
)

if created:
    print(f'✅ 已添加: {tool.name}')
else:
    print(f'⚠️  已存在: {tool.name}')
