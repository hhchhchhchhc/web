#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool, Category

category = Category.objects.get(id=706)

tools_data = [
    {
        'name': 'Any Router - 新用户$100免费额度',
        'slug': 'anyrouter-100-credit',
        'short_description': '聚合多个AI模型的平台，新用户注册送$100额度，支持Claude 3.5 Sonnet、Opus等，API兼容OpenAI格式',
        'full_description': '''Any Router - 新用户$100免费额度

✅ 推荐指数：⭐⭐⭐⭐

免费额度：新用户注册送$100
支持模型：Claude 3.5 Sonnet、Opus等多个版本
特点：聚合多个AI模型，一个API调用所有模型

使用方法：
1. 访问 anyrouter.ai 注册账号
2. 完成邮箱验证，自动获得$100额度
3. 在控制台创建API密钥
4. 使用OpenAI兼容格式调用Claude模型

优势：
• 额度充足，$100可使用较长时间
• 支持多种模型切换
• API格式兼容OpenAI，易于集成
• 国内可直接访问''',
        'website_url': 'https://anyrouter.ai',
    },
    {
        'name': 'Puter.js - 完全免费的Claude API',
        'slug': 'puterjs-free-claude',
        'short_description': '开源云操作系统，内置AI功能，完全免费无限制使用Claude 3.5 Sonnet',
        'full_description': '''Puter.js - 完全免费的Claude API

✅ 推荐指数：⭐⭐⭐⭐

免费额度：完全免费，无限制使用
支持模型：Claude 3.5 Sonnet
特点：开源云操作系统，内置AI功能

使用方法：
1. 访问 puter.com 注册账号
2. 在应用中心找到AI助手
3. 通过JavaScript SDK调用Claude API
4. 完全免费，适合轻量级应用''',
        'website_url': 'https://puter.com',
    },
    {
        'name': 'OpenRouter - AI模型聚合平台',
        'slug': 'openrouter-ai-platform',
        'short_description': '模型聚合平台，支持Claude全系列+100+其他模型，价格比官方便宜30-50%',
        'full_description': '''OpenRouter - AI模型聚合平台

💡 推荐指数：⭐⭐⭐

免费额度：部分模型免费，Claude需付费但价格较低
支持模型：Claude全系列+100+其他模型
特点：模型聚合平台，价格透明

使用方法：
1. 访问 openrouter.ai 注册
2. 充值少量金额（$5起）
3. 获取API密钥
4. 按实际使用量付费，价格比官方便宜30-50%''',
        'website_url': 'https://openrouter.ai',
    },
]

print(f'准备添加 {len(tools_data)} 个第三方平台工具\n')

for tool_data in tools_data:
    existing = Tool.objects.filter(slug=tool_data['slug']).first()
    if existing:
        print(f'⏭️  跳过已存在: {tool_data["name"]}')
        continue

    tool = Tool.objects.create(
        name=tool_data['name'],
        slug=tool_data['slug'],
        short_description=tool_data['short_description'],
        full_description=tool_data['full_description'],
        website_url=tool_data['website_url'],
        category=category,
        is_featured=True,
        is_published=True,
    )
    print(f'✅ 成功添加: {tool.name}')

print('\n完成第三方平台工具添加！')
