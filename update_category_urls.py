#!/usr/bin/env python3
import os
import django
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category

html_file = os.path.expanduser('~/图片/aibot.html')
print(f'读取 {html_file}...\n')

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# 查找所有分类区块
category_data = []
h4_tags = soup.find_all('h4', class_='text-gray')

for h4 in h4_tags:
    cat_name = h4.get_text(strip=True)

    # 查找同级的"查看更多"链接
    parent = h4.parent
    if parent:
        link = parent.find('a', class_='btn-move')
        if link and link.get('href'):
            cat_url = link.get('href')
            category_data.append((cat_name, cat_url))

print(f'找到 {len(category_data)} 个分类\n')

updated = 0
for cat_name, cat_url in category_data:
    try:
        cat = Category.objects.get(name=cat_name)
        cat.url = cat_url
        cat.save()
        print(f'✓ {cat_name}: {cat_url}')
        updated += 1
    except Category.DoesNotExist:
        print(f'✗ 未找到分类: {cat_name}')

print(f'\n完成！更新了 {updated} 个分类的URL')
