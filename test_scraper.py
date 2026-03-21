#!/usr/bin/env python3
import os
import django
import subprocess
from bs4 import BeautifulSoup
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 读取已保存的首页
with open('/tmp/ai-bot.html', 'r', encoding='utf-8') as f:
    homepage_html = f.read()

soup = BeautifulSoup(homepage_html, 'html.parser')

# 提取工具链接
cards = soup.find_all('div', class_='url-card')
print(f'找到 {len(cards)} 个工具卡片\n')

# 只处理前5个作为测试
for i, card in enumerate(cards[:5], 1):
    link = card.find('a')
    if not link or not link.get('href'):
        continue

    detail_url = link.get('href')
    if not detail_url.startswith('https://ai-bot.cn/sites/'):
        continue

    print(f'{i}. 获取 {detail_url}')

    # 使用curl获取详情页
    result = subprocess.run(['curl', '-s', '-L', detail_url],
                          capture_output=True, text=True, timeout=30)

    if result.returncode != 0:
        print(f'   失败: {result.returncode}')
        continue

    # 解析详情页
    detail_soup = BeautifulSoup(result.stdout, 'html.parser')

    # 提取信息
    title = detail_soup.find('h1', class_='post-title')
    name = title.get_text(strip=True) if title else '未知'

    go_link = detail_soup.find('a', class_='go-link')
    website_url = go_link.get('href') if go_link else detail_url

    cat_link = detail_soup.find('a', rel='category tag')
    category_name = cat_link.get_text(strip=True) if cat_link else 'AI工具'

    print(f'   名称: {name}')
    print(f'   URL: {website_url}')
    print(f'   分类: {category_name}\n')

print('测试完成')
