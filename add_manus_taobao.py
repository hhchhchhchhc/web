#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category = Category.objects.get(name='赚钱技巧')

tool_data = {
    'name': 'Manus AI淘宝售卖攻略',
    'short_description': '手机端淘宝上架Manus AI完整流程，从注册店铺到完成售卖',
    'full_description': '''**变现方式：**
在淘宝上售卖Manus AI相关服务或教程，完整的手机端操作流程。

**完整流程包括：**
- 淘宝店铺注册
- 商品上架设置
- Manus AI服务包装
- 售卖完整流程
- 手机端操作教程

**教程特点：**
- 超详细手机版教程
- 无废话全套流程
- 包含谷歌账号注册指导
- 实操性强

**注意事项：**
目前Manus AI需要邀请码才能进入使用

**教程链接：**
腾讯文档提供完整攻略''',
    'website_url': 'https://docs.qq.com/doc/DVGxwR2pEdHZXYUpZ',
    'category': category
}

tool, created = Tool.objects.get_or_create(
    name=tool_data['name'],
    defaults=tool_data
)

if created:
    print(f'✓ 已添加: {tool.name} → {category.name}')
else:
    print(f'- 已存在: {tool.name}')

print('\n完成！')
