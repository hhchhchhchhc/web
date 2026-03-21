#!/usr/bin/env python3
import os

import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool


category, _ = Category.objects.get_or_create(
    name='免费用最高级大模型',
    defaults={
        'slug': slugify('免费用最高级大模型', allow_unicode=True),
        'description': '免费使用 Claude Opus 等顶级 AI 模型的方法',
    },
)

tool, created = Tool.objects.update_or_create(
    slug='agentrouter-225-credit',
    defaults={
        'name': 'AgentRouter 注册送 $225',
        'short_description': '注册送 $225，可用 Claude Opus 等顶级模型，适合需要聚合路由和高质量模型额度的用户',
        'full_description': '''AgentRouter - 注册送 $225 Claude Opus 额度

✅ 推荐指数：⭐⭐⭐⭐

免费额度：注册即送 $225
支持模型：Claude Opus 等顶级模型
特点：模型聚合路由，适合需要高质量模型和统一调用入口的场景

使用方法：
1. 访问 agentrouter.org 注册账号
2. 完成基础注册流程后领取赠送额度
3. 在控制台查看可用模型和额度情况
4. 按平台提供的方式调用 Claude Opus 等模型

适合场景：
• 想低成本体验高阶 Claude 模型
• 需要统一路由多个模型
• 做 OpenClaw、自动化工作流或 API 调用测试''',
        'website_url': 'https://agentrouter.org/',
        'category': category,
        'is_featured': True,
        'is_published': True,
    },
)

print(f'{"创建" if created else "更新"}成功: {tool.name}')
