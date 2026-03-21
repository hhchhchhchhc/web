#!/usr/bin/env python3
import os
import django
from bs4 import BeautifulSoup
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

html_file = os.path.expanduser('~/图片/aibot.html')
print(f'导入 {html_file}...\n')

with open(html_file, 'r', encoding='utf-8') as f:
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

print(f'分类: {len(categories)} 个')

# 提取工具
cards = soup.find_all('div', class_='url-card')
print(f'工具卡片: {len(cards)} 个\n')

imported = 0
skipped = 0

for card in cards:
    link = card.find('a')
    if not link:
        continue

    title = link.get('title', '')
    href = link.get('href', '')
    name_span = link.find('span', class_='text-muted')
    name = name_span.get_text(strip=True) if name_span else title[:50]

    if not name or not href:
        continue

    if Tool.objects.filter(website_url=href).exists():
        skipped += 1
        continue

    category = list(categories.values())[0] if categories else None
    if not category:
        continue

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

    if imported % 100 == 0:
        print(f'已导入 {imported}...')

print(f'\n✓ 完成')
print(f'导入: {imported}')
print(f'跳过: {skipped}')
