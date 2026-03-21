#!/usr/bin/env python3
import os
import django
from bs4 import BeautifulSoup
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 删除空分类
print('删除空分类...')
empty_cats = Category.objects.filter(tools__isnull=True).delete()
print(f'✓ 删除了 {empty_cats[0]} 个空分类')

# 删除书签栏分类及其书签
print('\n删除书签栏分类...')
bookmarks_bar = Category.objects.filter(name='书签栏').delete()
print(f'✓ 删除了 {bookmarks_bar[0]} 个分类及书签')

# 重新导入
html_file = os.path.expanduser('~/图片/bookmarks_2026_2_5.html')
print(f'\n解析 {html_file}...')

with open(html_file, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

bookmarks = []
for h3 in soup.find_all('h3'):
    cat_name = h3.get_text(strip=True)
    parent_dt = h3.find_parent('dt')
    if parent_dt:
        sub_dl = parent_dt.find('dl')
        if sub_dl:
            for a in sub_dl.find_all('a', href=True):
                name = a.get_text(strip=True)
                url = a.get('href')
                if name and url and not url.startswith('javascript:'):
                    bookmarks.append({'category': cat_name, 'name': name, 'url': url})

print(f'找到 {len(bookmarks)} 个书签')

print('\n导入数据库...')
stats = {'categories': 0, 'tools': 0, 'skipped': 0}
categories_cache = {}

for bookmark in bookmarks:
    cat_name = bookmark['category']
    if cat_name not in categories_cache:
        category, created = Category.objects.get_or_create(
            name=cat_name,
            defaults={'slug': slugify(cat_name, allow_unicode=True)}
        )
        categories_cache[cat_name] = category
        if created:
            stats['categories'] += 1
    category = categories_cache[cat_name]
    if Tool.objects.filter(website_url=bookmark['url']).exists():
        stats['skipped'] += 1
        continue
    base_slug = slugify(bookmark['name'], allow_unicode=True) or f"tool-{hash(bookmark['url'])}"
    slug = base_slug
    counter = 1
    while Tool.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    Tool.objects.create(
        name=bookmark['name'],
        slug=slug,
        short_description=f"来自书签: {bookmark['name']}",
        website_url=bookmark['url'],
        category=category,
        is_published=True
    )
    stats['tools'] += 1
    if stats['tools'] % 100 == 0:
        print(f"  已导入 {stats['tools']} 个书签...")

print(f'\n✓ 完成！')
print(f'  新增分类: {stats["categories"]}')
print(f'  新增书签: {stats["tools"]}')
print(f'  跳过重复: {stats["skipped"]}')
