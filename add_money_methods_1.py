#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category = Category.objects.get(name='赚钱技巧')

tools_data = [
    {
        'name': 'AI虚拟资料售卖变现法',
        'short_description': '利用AI制作学科知识卡片，打包售卖虚拟资料月入过万',
        'full_description': '''**操作方法：**
1. 选择垂直领域：针对特定学科（如七年级地理、历史）制作知识卡片
2. 使用AI工具：利用Nano Banana Pro等AI生图工具生成精美的知识卡片
3. 内容制作：将知识点可视化，制作成易于记忆的卡片形式
4. 打包售卖：在小红书、闲鱼等平台售卖虚拟资料包
5. 定价策略：单份9.9-19.9元，打包优惠

**成功案例：**
有创作者针对初中生制作地理、历史知识卡片，打包售卖虚拟资料变现近万元。

**关键要点：**
- 锁定精准人群（如初一学生家长）
- 内容要精美且实用
- 持续更新内容增加复购''',
        'website_url': 'http://ai-tool.indevs.in/',
        'category': category
    },
    {
        'name': 'AI生日涂鸦照片变现',
        'short_description': '在小红书售卖AI生成的生日涂鸦照，单链销量过万利润超13万',
        'full_description': '''**操作方法：**
1. 使用工具：Nano Banana Pro或Seedance 2.0生成生日涂鸦风格照片
2. 制作流程：
   - 客户提供照片
   - AI生成涂鸦风格的生日祝福图
   - 添加个性化祝福语
3. 销售平台：小红书开店或私信接单
4. 定价：单张9.9元
5. 引流：发布作品案例吸引客户

**成功数据：**
单链销量过万，利润超13万元

**关键要点：**
- 注重情绪价值>实用价值
- 图片要精美有创意
- 快速交付提升复购率''',
        'website_url': 'http://ai-tool.indevs.in/',
        'category': category
    },
]

for tool_data in tools_data:
    tool, created = Tool.objects.get_or_create(
        name=tool_data['name'],
        defaults=tool_data
    )

    if created:
        print(f'✓ 已添加: {tool.name}')
    else:
        print(f'- 已存在: {tool.name}')

print('\n第一批赚钱技巧完成！')
