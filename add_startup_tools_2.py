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

# 3. V2EX酷工作版块
Tool.objects.get_or_create(
    name='V2EX酷工作',
    defaults={
        'slug': 'v2ex-jobs',
        'short_description': '技术社区酷工作版块，大量技术变现和远程工作分享',
        'full_description': '''💼 V2EX酷工作 - 技术人的变现宝库

💰 核心价值：
• 真实的技术变现案例分享
• 远程工作和自由职业机会
• 独立开发者收入经验交流

✨ 主要内容：
• 技术接单和外包经验
• 独立产品开发分享
• 远程工作机会发布
• 技术创业讨论

🎯 适用人群：
• 想要技术变现的开发者
• 寻找远程工作的技术人
• 独立开发者和自由职业者''',
        'website_url': 'https://www.v2ex.com/go/jobs',
        'category': startup_category,
        'is_published': True,
        'is_featured': True
    }
)

# 4. Polymarket
Tool.objects.get_or_create(
    name='Polymarket',
    defaults={
        'slug': 'polymarket',
        'short_description': '预测市场平台，通过市场数据验证认知和判断',
        'full_description': '''📊 Polymarket - 用市场验证认知

🎯 核心价值：
• 通过真金白银的预测市场验证想法
• 了解大众对各类事件的真实看法
• 训练决策和判断能力

✨ 主要功能：
• 各类事件的预测市场
• 实时赔率反映市场共识
• 参与预测赚取收益
• 数据驱动的决策参考

🎯 适用场景：
• 验证商业想法和假设
• 了解市场趋势和共识
• 训练概率思维
• 寻找投资机会''',
        'website_url': 'https://polymarket.com',
        'category': startup_category,
        'is_published': True,
        'is_featured': True
    }
)

print("✅ 第二批工具添加成功！")
