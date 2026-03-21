#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# Create category
category, _ = Category.objects.get_or_create(
    name='免费资源',
    defaults={'slug': slugify('免费资源', allow_unicode=True)}
)

# Create tool
Tool.objects.get_or_create(
    name='Stackryze免费域名',
    defaults={
        'slug': slugify('Stackryze免费域名', allow_unicode=True),
        'short_description': '免费注册域名，每个账号最多5个域名，每个域名1年免费使用期',
        'full_description': '''🚨 免费域名福利（有效期 1 年）

目前你可以一次性免费注册最多 5 个域名，每个域名都可使用 1 年时间，非常适合用来折腾各种项目和想法 😎

👉 你可以获得：
• 每个账号最多 5 个免费域名 🎁
• 每个域名 1 年免费注册期限 ⏳

🛠 适合用于：
• 个人副业项目、练手项目、小工具网站 💡
• 各类机器人 / 接口服务（Bots / APIs）🤖
• 测试环境、演示站点、Demo 展示 🧪
• 临时部署、MVP 验证、想法快速上线 🚀

⚠️ 注意事项：
比较适合做测试、实验、小项目，不太建议做长期品牌或核心业务主域名 🔐''',
        'website_url': 'https://domain.stackryze.com/',
        'category': category,
        'is_published': True,
        'is_featured': True
    }
)

print("✅ 免费域名工具添加成功！")
