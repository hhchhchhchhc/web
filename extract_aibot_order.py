#!/usr/bin/env python3
import os
import django
from bs4 import BeautifulSoup
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

html_file = os.path.expanduser('~/图片/aibot.html')
with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

category_tools = {}
h4_tags = soup.find_all('h4', class_='text-gray')

for h4 in h4_tags:
    cat_name = h4.get_text(strip=True)

    # 找到h4后面的row div
    current = h4.parent
    while current:
        current = current.find_next_sibling()
        if current and current.name == 'div' and 'row' in current.get('class', []):
            break

    if not current:
        continue

    tools = []
    cards = current.find_all('div', class_='url-card')

    for card in cards:
        link = card.find('a')
        if link:
            url = link.get('data-url', '')
            if url and not url.startswith('https://ai-bot.cn/sites/'):
                tools.append(url)

    if tools:
        category_tools[cat_name] = tools
        print(f'{cat_name}: {len(tools)} 个工具')

with open('/tmp/aibot_tool_order.json', 'w', encoding='utf-8') as f:
    json.dump(category_tools, f, ensure_ascii=False, indent=2)

print(f'\n已保存')
