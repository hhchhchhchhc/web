#!/usr/bin/env python3
import os
import django
from bs4 import BeautifulSoup
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

print('从ai-bot.cn首页导入工具...\n')

# 读取已保存的首页
with open('/tmp/ai-bot.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# 提取分类
categories = {}
for h4 in soup.find_all('h4', class_='text-gray'):
    cat_name = h4.get_text(strip=True)
    if cat_name:
        cat, _ = Category.objects.get_or_create(
            name=cat_name,
            defaults={'slug': slugify(cat_name, allow_unicode=True)}
        )
        categories[cat_name] = cat

print(f'创建/获取 {len(categories)} 个分类')

# 提取工具
cards = soup.find_all('div', class_='url-card')
print(f'找到 {len(cards)} 个工具\n')

imported = 0
skipped = 0

for card in cards:
    link = card.find('a')
    if not link:
        continue

    # 提取信息
    title = link.get('title', '')
    href = link.get('href', '')

    # 提取名称
    name_span = link.find('span', class_='text-muted')
    name = name_span.get_text(strip=True) if name_span else title[:50]

    if not name or not href:
        continue

    # 检查重复
    if Tool.objects.filter(website_url=href).exists():
        skipped += 1
        continue

    # 使用第一个分类
    category = list(categories.values())[0] if categories else None
    if not category:
        continue

    # 创建工具
    slug = slugify(name, allow_unicode=True) or f"tool-{imported}"
    counter = 1
    while Tool.objects.filter(slug=slug).exists():
        slug = f"{slugify(name, allow_unicode=True)}-{counter}"
        counter += 1

    Tool.objects.create(
        name=name,
        slug=slug,
        short_description=title[:300] if title else name,
        full_description=title if title else name,
        website_url=href,
        category=category,
        is_published=True
    )
    imported += 1

    if imported % 50 == 0:
        print(f'已导入 {imported} 个工具...')

print(f'\n✓ 完成！')
print(f'  导入工具: {imported}')
print(f'  跳过重复: {skipped}')
