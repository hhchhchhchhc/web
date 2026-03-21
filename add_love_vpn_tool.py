#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category, _ = Category.objects.get_or_create(
    name='免费赠送VPN',
    defaults={'slug': slugify('免费赠送VPN', allow_unicode=True)}
)

tool, created = Tool.objects.update_or_create(
    name='免费优质VPN（Love）',
    defaults={
        'slug': slugify('免费优质VPN（Love）', allow_unicode=True),
        'short_description': '注册后可免费使用，进 Telegram 群获取兑换码',
        'full_description': '''免费优质VPN

注册链接：
https://love.p6m6.com/#/register?code=qCinW7Bn

群组：
https://t.me/pokemon_love

加群可获取兑换码后免费使用。''',
        'website_url': 'https://love.p6m6.com/#/register?code=qCinW7Bn',
        'category': category,
        'is_published': True,
        'is_featured': True,
    }
)

print(f"{'✅ 已新增' if created else '✅ 已更新'}: {tool.name}")
print(f"   分类: {tool.category.name}")
print(f"   URL: {tool.website_url}")
print(f"   Slug: {tool.slug}")
