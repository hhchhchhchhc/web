#!/usr/bin/env python3
import os

import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool


model_category, _ = Category.objects.get_or_create(
    name='免费用最高级大模型',
    defaults={
        'slug': slugify('免费用最高级大模型', allow_unicode=True),
        'description': '免费使用 Claude Opus 等顶级 AI 模型的方法',
    },
)

api_category, _ = Category.objects.get_or_create(
    name='开发者资源',
    defaults={
        'slug': slugify('开发者资源', allow_unicode=True),
        'description': 'API、自动化与开发相关资源',
    },
)

tools = [
    {
        'slug': 'anyrouter-top-checkin',
        'name': 'AnyRouter 公益站',
        'category': model_category,
        'short_description': '目前能用的老牌公益站，支持自动签到；可配合开源签到项目长期白嫖',
        'full_description': '''AnyRouter 公益站

✅ 推荐指数：⭐⭐⭐⭐

可用性：目前能用，老牌入口，适合长期观察
特点：支持自动签到，适合日常白嫖模型额度
注册地址：https://anyrouter.top/register?aff=0FzF
自动签到项目：https://github.com/KimYx0207/anyrouter-check-in

使用方法：
1. 访问 anyrouter.top/register?aff=0FzF 注册
2. 登录后开启日常签到
3. 需要自动化时可用开源签到项目
4. 开源项目在 Fork 原版基础上增加 Win 本地每日签到能力

适合场景：
• 低成本拿模型额度
• 本地自动签到保活
• 作为 OpenClaw / API 测试备用入口''',
        'website_url': 'https://anyrouter.top/register?aff=0FzF',
    },
    {
        'slug': 'agentrouter-225-credit',
        'name': 'AgentRouter 公益站',
        'category': model_category,
        'short_description': '老牌复活入口，目前可冲；AnyRouter 和 AgentRouter 不是同一个站',
        'full_description': '''AgentRouter 公益站

✅ 推荐指数：⭐⭐⭐⭐

可用性：老牌复活，目前可冲，但稳定时间未知
特点：和 AnyRouter 不是同一个站，适合多备一个公益入口
注册地址：https://agentrouter.org/register?aff=rLco

使用方法：
1. 访问 agentrouter.org/register?aff=rLco 注册
2. 登录后查看当前可用模型和额度
3. 适合作为高阶模型与聚合路由的备用入口

适合场景：
• 公益站多开备用
• 低成本体验高阶模型
• 接 OpenClaw、自动化工作流或 API 调用测试''',
        'website_url': 'https://agentrouter.org/register?aff=rLco',
    },
    {
        'slug': 'gemai-api-public',
        'name': 'GemAI 公益 API',
        'category': api_category,
        'short_description': '目前能用的公益 API 注册入口，适合开发调试和低成本接工作流',
        'full_description': '''GemAI 公益 API

✅ 推荐指数：⭐⭐⭐⭐

可用性：目前能用
特点：公益 API 入口，适合开发调试和工作流接入
注册地址：https://api.gemai.cc/register?aff=gTcX

使用方法：
1. 访问 api.gemai.cc/register?aff=gTcX 注册
2. 登录后台获取 API 相关信息
3. 用于本地开发、脚本测试或自动化工作流接入

适合场景：
• 免费 API 调试
• OpenClaw / 脚本工作流接入
• 作为常用厂商之外的备用 API 入口''',
        'website_url': 'https://api.gemai.cc/register?aff=gTcX',
    },
]

for data in tools:
    tool, created = Tool.objects.update_or_create(
        slug=data['slug'],
        defaults={
            'name': data['name'],
            'short_description': data['short_description'],
            'full_description': data['full_description'],
            'website_url': data['website_url'],
            'category': data['category'],
            'is_featured': True,
            'is_published': True,
        },
    )
    print(f'{"创建" if created else "更新"}成功: {tool.name}')
