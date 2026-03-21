#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 获取账号服务分类
category, _ = Category.objects.get_or_create(
    name='账号服务',
    defaults={'slug': slugify('账号服务', allow_unicode=True)}
)

# 1. 5sim接码平台
Tool.objects.get_or_create(
    name='5sim接码平台',
    defaults={
        'slug': slugify('5sim接码平台', allow_unicode=True),
        'short_description': '超低价接码平台，七毛一个，支持多国手机号验证',
        'full_description': '''📱 5sim - 超低价接码平台

💰 价格优势：
• 仅需七毛钱即可接收验证码
• 支持全球多个国家和地区
• 价格透明，按次计费

✨ 主要功能：
• 临时手机号接收验证码
• 支持各类平台注册验证
• 快速接收，实时更新
• 多国号码可选

🎯 适用场景：
• 账号注册验证
• 隐私保护
• 批量注册需求
• 测试开发''',
        'website_url': 'https://5sim.net/zh',
        'category': category,
        'is_published': True,
        'is_featured': True
    }
)

# 2. Hero SMS接码平台
Tool.objects.get_or_create(
    name='Hero SMS接码平台',
    defaults={
        'slug': slugify('Hero SMS接码平台', allow_unicode=True),
        'short_description': '几毛钱一个的接码平台，性价比高，有时有效',
        'full_description': '''📱 Hero SMS - 经济实惠接码平台

💰 价格优势：
• 几毛钱即可接收验证码
• 性价比极高
• 多种套餐可选

⚠️ 使用说明：
• 服务有时有效，建议配合其他平台使用
• 适合预算有限的用户
• 建议先小额测试

✨ 主要功能：
• 临时手机号验证码接收
• 支持主流平台注册
• 价格实惠

🎯 适用场景：
• 账号注册
• 验证码接收
• 测试用途''',
        'website_url': 'https://hero-sms.com/cn/services',
        'category': category,
        'is_published': True,
        'is_featured': True
    }
)

print("✅ 接码平台工具添加成功！")
print("- 5sim接码平台 (账号服务)")
print("- Hero SMS接码平台 (账号服务)")
